from sqlalchemy.orm import Session

from app.crud.crud_account import crud_account
from app.schemas.schema_summary import SchemaSummary
from app.services.email_service import EmailService


class NotifyTransactionSummary:
    def __init__(self, db: Session, data: SchemaSummary):
        self._db = db
        self._data = data

    def notify(self):
        content = ""
        account_id = None
        for account_summary in self._data.months_summary:
            if account_id != account_summary.account_id:
                account_id = account_summary.account_id
                email = crud_account.get(self._db, account_id).email
                if content:
                    self.send_email(content, email)
                content = ""
            content = self.__create_html_content(account_summary, content)
        self.send_email(content, email)

    def send_email(self, html_content: str, email: str):
        EmailService().send_email(html_content, email, subject="Consolidated Summary")

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
