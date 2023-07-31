from sqlalchemy.orm import Session

from app.crud.crud_account import crud_account
from app.crud.crud_transaction import crud_transaction
from app.schemas.schema_summary import SchemaSummary
from app.services.email_service import EmailService


class NotifyTransactionSummary:
    def __init__(self, db: Session, data: SchemaSummary):
        self._db = db
        self._data = data
        self._emails = []

    def notify(self):
        self.create_emails_content()
        self.send_email()

    def create_emails_content(self):
        content = ""
        txn_ids = []
        account_id = None

        for account_summary in self._data.months_summary:
            if account_id != account_summary.account_id:
                account_id = account_summary.account_id
                email = crud_account.get(self._db, account_id).email
                if content:
                    self._emails.append((content, email, txn_ids))
                content = ""
                txn_ids = []
            txn_ids.extend(account_summary.transactions_ids)
            content = self.__create_html_content(account_summary, content)
        self._emails.append((content, email, txn_ids))

    def send_email(self):
        service = EmailService()
        for email in self._emails:
            try:
                service.send_email(email[0], email[1], subject="Consolidated Summary")
                crud_transaction.update_transactions_notified(self._db, txn_ids=email[2])
            except Exception as error:
                print(f"Error sending email to {email[1]}: {error}")

    def __create_html_content(self, summary, html_content):
        if not html_content:
            html_content = self.__create_base_content()

        html_content = html_content.replace("<month></month>", self.__create_month_content(summary))
        return html_content

    def __create_base_content(self):
        base_content = """
        <base>
        <head></head>
        <body>
            <month></month>
        </body>
        </base>
        """
        return base_content

    def __create_month_content(self, summary):
        month_content = f"""
            <h1>Consolidated Summary {summary.month} {summary.year} </h1>
            <p>Balance: {summary.balance}</p>
            <p>Number of Transactions in {summary.month}: {summary.transactions}</p>
            <p>Average Debit Amount: {summary.average_debit}</p>
            <p>Average Credit Amount: {summary.average_credit}</p>
            <img src="cid:stori_logo" alt="Stori Logo">
            <month></month>
        """
        return month_content
