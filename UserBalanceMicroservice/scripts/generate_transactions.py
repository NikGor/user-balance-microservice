import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserBalanceMicroservice.settings')
django.setup()

from django.contrib.auth.models import User
from UserBalanceMicroservice import settings
from UserBalanceMicroservice.transactions.models import Transaction
import random
from openai import OpenAI


def generate_transaction_comments():
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct-0914",
        prompt="сгенерируй 20 случайных комментариев к транзакции как в реальной платежной системе сервиса объявлений, "
               "на английском языке.\nнапример:\nPayment for item in ad #\nTransfer of funds, amount: "
               "$Invoice paid for ad #\nMoney sent for the advertised item\nSuccessful transaction for ad "
               "#\nPaid for the ad, transaction ID: #\nFunds transferred for the listed item\nPayment made "
               "for ad posting, amount: \nMoney sent for the product in ad #\nInvoice settled for "
               "ad #",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    comments = response.choices[0].text.strip().split('\n')
    return comments


def create_transactions():
    users = User.objects.all()
    comments = generate_transaction_comments()

    for user in users:
        for _ in range(random.randint(10, 30)):
            comment = random.choice(comments)
            Transaction.objects.create(
                user=user,
                amount=random.uniform(10, 500),
                transaction_type=random.choice(['deposit', 'withdraw', 'transfer']),
                comment=comment,
                status=random.choice(['completed', 'pending', 'failed'])
            )

        print(f"Created transactions for {user.username}")


if __name__ == "__main__":
    create_transactions()
