"""
Signals to automatically sync Exam Results with Scores for promotion
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ExamResult, Score
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ExamResult)
def sync_exam_result_to_score(sender, instance, created, **kwargs):
    """
    Automatically create/update Score when ExamResult is saved
    This connects Exam system with Student Promotion
    """
    # Only sync if student was present
    if not instance.was_present:
        logger.info(f"Skipping sync for {instance.student} - was absent")
        return
    
    exam = instance.exam
    student = instance.student
    
    try:
        # Get or create corresponding Score
        score, score_created = Score.objects.update_or_create(
            student=student,
            subject=exam.subject,
            exam_type=exam.exam_type,
            exam=exam,
            academic_year=exam.academic_year,
            defaults={
                'score': instance.score,
                'max_score': exam.max_score,
                'remarks': instance.remarks or ''
            }
        )
        
        if score_created:
            logger.info(f"✅ Created Score for {student} - {exam.subject} - {exam.exam_type}")
        else:
            logger.info(f"🔄 Updated Score for {student} - {exam.subject} - {exam.exam_type}")
            
    except Exception as e:
        logger.error(f"❌ Error syncing ExamResult to Score: {str(e)}")


@receiver(post_delete, sender=ExamResult)
def delete_score_on_exam_result_delete(sender, instance, **kwargs):
    """
    Delete corresponding Score when ExamResult is deleted
    """
    try:
        # Find and delete matching score
        scores = Score.objects.filter(
            student=instance.student,
            subject=instance.exam.subject,
            exam_type=instance.exam.exam_type,
            exam=instance.exam,
            academic_year=instance.exam.academic_year
        )
        
        deleted_count = scores.count()
        scores.delete()
        
        if deleted_count > 0:
            logger.info(f"🗑️  Deleted {deleted_count} Score(s) for {instance.student} - {instance.exam.subject}")
            
    except Exception as e:
        logger.error(f"❌ Error deleting Score: {str(e)}")
