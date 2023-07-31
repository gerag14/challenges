from sqlalchemy.orm import Session

from app.core.notify_transactions_summary import NotifyTransactionSummary

from .test_transactions_summary import create_random_summary


def tests_content_html(db: Session):
    data_summary, txn = create_random_summary(db=db)
    email_class_obj = NotifyTransactionSummary(db=db, data=data_summary)
    assert email_class_obj
    assert not email_class_obj._emails
    email_class_obj.create_emails_content()
    assert email_class_obj._emails
