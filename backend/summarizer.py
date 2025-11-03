"""
NLP-based email thread summarization service using Hugging Face Transformers
"""
import re
from typing import List, Dict, Tuple
from transformers import pipeline
from models import Thread, ThreadSummary


class EmailSummarizer:
    """
    Email thread summarizer using Hugging Face BART model for summarization
    and rule-based extraction for structured data.
    """

    def __init__(self):
        """Initialize the summarizer with BART model"""
        print("Loading summarization model (this may take a few minutes on first run)...")
        try:
            # Use BART for abstractive summarization
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU (-1), change to 0 for GPU
            )
            print("✓ Summarization model loaded successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not load BART model: {e}")
            print("   Using fallback extractive summarization")
            self.summarizer = None

    def summarize_thread(self, thread: Thread) -> ThreadSummary:
        """
        Generate a comprehensive summary of an email thread

        Args:
            thread: Email thread to summarize

        Returns:
            ThreadSummary with all extracted information
        """
        # Combine all messages into one text
        full_text = self._prepare_text(thread)

        # Generate summary using BART or fallback
        summary_text = self._generate_summary(full_text, thread)

        # Extract structured information
        sentiment = self._analyze_sentiment(full_text)
        action_items = self._extract_action_items(thread)
        priority = self._calculate_priority(full_text, thread)
        issue_category = self._categorize_issue(thread)
        status = self._determine_status(full_text)

        return ThreadSummary(
            thread_id=thread.thread_id,
            order_id=thread.order_id,
            product=thread.product,
            issue_category=issue_category,
            summary=summary_text,
            sentiment=sentiment,
            status=status,
            action_items=action_items,
            priority=priority
        )

    def _prepare_text(self, thread: Thread) -> str:
        """Combine all messages and clean noisy data"""
        messages = []
        for msg in thread.messages:
            # Add sender context
            sender = "Customer" if msg.sender == "customer" else "Company"
            messages.append(f"{sender}: {msg.body}")

        return " ".join(messages)

    def _generate_summary(self, full_text: str, thread: Thread) -> str:
        """Generate human-readable summary"""
        if self.summarizer is None:
            # Fallback: extractive summary
            return self._fallback_summary(full_text, thread)

        try:
            # Clean text - remove obvious noise (standalone numbers)
            cleaned_text = self._clean_noisy_text(full_text)

            # Truncate if too long (BART max: 1024 tokens)
            max_chars = 3000
            if len(cleaned_text) > max_chars:
                cleaned_text = cleaned_text[:max_chars]

            # Generate summary
            result = self.summarizer(
                cleaned_text,
                max_length=130,
                min_length=30,
                do_sample=False
            )

            summary = result[0]['summary_text']

            # Add order and product context
            context = f"Customer contact regarding {thread.product} (Order #{thread.order_id}). "
            return context + summary

        except Exception as e:
            print(f"⚠️  Summarization error: {e}, using fallback")
            return self._fallback_summary(full_text, thread)

    def _clean_noisy_text(self, text: str) -> str:
        """Remove noise from email text (random numbers, etc.)"""
        # Remove standalone numbers (likely noise)
        text = re.sub(r'\b\d{3,5}\b', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _fallback_summary(self, full_text: str, thread: Thread) -> str:
        """Simple rule-based summary when model is unavailable"""
        # Extract key sentences with action words
        action_keywords = [
            'damaged', 'broken', 'delayed', 'wrong', 'return',
            'refund', 'replace', 'issue', 'problem', 'help'
        ]

        sentences = full_text.split('.')
        key_sentences = []

        for sentence in sentences[:5]:  # Check first 5 sentences
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in action_keywords):
                key_sentences.append(sentence.strip())

        if key_sentences:
            summary = ". ".join(key_sentences[:2]) + "."
        else:
            summary = f"Customer inquiry about {thread.product} order {thread.order_id}."

        return summary

    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment using keyword matching"""
        text_lower = text.lower()

        # Negative/frustrated indicators
        negative_words = ['damaged', 'broken', 'wrong', 'delayed', 'issue',
                         'problem', 'frustrated', 'angry', 'disappointed']
        negative_count = sum(1 for word in negative_words if word in text_lower)

        # Positive indicators
        positive_words = ['resolved', 'thank', 'thanks', 'appreciate',
                         'good', 'great', 'satisfied']
        positive_count = sum(1 for word in positive_words if word in text_lower)

        # Neutral indicators
        neutral_words = ['confirm', 'update', 'question', 'inquiry', 'status']
        neutral_count = sum(1 for word in neutral_words if word in text_lower)

        if negative_count > positive_count + 2:
            return "frustrated"
        elif negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"

    def _extract_action_items(self, thread: Thread) -> List[str]:
        """Extract action items based on issue type"""
        topic = thread.topic.lower()

        action_map = {
            'damaged': [
                'Request customer photos of damage',
                'Process replacement order',
                'Initiate carrier claim for damaged shipment'
            ],
            'late delivery': [
                'Check tracking with carrier',
                'Provide updated ETA to customer',
                'Consider expedited shipping for replacement if lost'
            ],
            'wrong': [
                'Generate return label',
                'Process exchange order for correct variant',
                'Verify correct SKU for replacement'
            ],
            'return': [
                'Send return label to customer',
                'Process refund upon item receipt',
                'Verify return policy timeframe'
            ],
            'address': [
                'Confirm shipping address with customer',
                'Update address in system',
                'Resume order fulfillment'
            ]
        }

        for keyword, actions in action_map.items():
            if keyword in topic:
                return actions

        # Default actions
        return [
            'Review customer inquiry',
            'Contact customer for clarification',
            'Update ticket status'
        ]

    def _calculate_priority(self, text: str, thread: Thread) -> str:
        """Calculate priority based on urgency indicators"""
        text_lower = text.lower()

        # High priority indicators
        high_priority = ['urgent', 'immediately', 'asap', 'damaged',
                        'broken', 'not received', 'never arrived']
        high_count = sum(1 for word in high_priority if word in text_lower)

        # Medium priority indicators
        medium_priority = ['delayed', 'wrong', 'incorrect', 'missing']
        medium_count = sum(1 for word in medium_priority if word in text_lower)

        # Number of messages also indicates priority
        message_count = len(thread.messages)

        if high_count >= 2 or message_count >= 7:
            return "high"
        elif high_count >= 1 or medium_count >= 1 or message_count >= 5:
            return "high"
        else:
            return "medium"

    def _categorize_issue(self, thread: Thread) -> str:
        """Categorize the issue type"""
        topic = thread.topic.lower()

        categories = {
            'damaged': 'Product Damage',
            'delivery': 'Delivery Issue',
            'late': 'Delivery Issue',
            'wrong': 'Wrong Item',
            'return': 'Return/Refund',
            'refund': 'Return/Refund',
            'address': 'Address Verification',
            'shipping': 'Shipping Issue'
        }

        for keyword, category in categories.items():
            if keyword in topic:
                return category

        return 'General Inquiry'

    def _determine_status(self, text: str) -> str:
        """Determine resolution status"""
        text_lower = text.lower()

        if 'resolved' in text_lower or 'approved' in text_lower:
            return 'resolved'
        elif 'pending' in text_lower or 'confirm' in text_lower:
            return 'pending'
        else:
            return 'in_progress'


# Global instance
_summarizer_instance = None


def get_summarizer() -> EmailSummarizer:
    """Get or create singleton summarizer instance"""
    global _summarizer_instance
    if _summarizer_instance is None:
        _summarizer_instance = EmailSummarizer()
    return _summarizer_instance
