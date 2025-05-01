from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from Companies.models import Company
from Invoices.models import Invoice, InvoiceItem
from Services.models import Service



class Command(BaseCommand):
    help = "Generate monthly invoices for each company based on non-invoiced services."

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Determine the previous month (handle January rollover)
        if today.month == 1:
            invoice_month = 12
            invoice_year = today.year - 1
        else:
            invoice_month = today.month - 1
            invoice_year = today.year

        self.stdout.write(f"Generating invoices for {invoice_month}/{invoice_year}")

        companies = Company.objects.all()
        for company in companies:
            # Get all services created in the previous month that haven't been invoiced
            services_to_invoice = Service.objects.filter(
                company=company,
                created_at__year=invoice_year,
                created_at__month=invoice_month,
                is_invoiced=False
            )
            
            if not services_to_invoice.exists():
                continue

            # Set a deadline 30 days from now (adjust as needed)
            deadline = timezone.now() + timedelta(days=30)
            
            # Create an invoice for the company
            invoice = Invoice.objects.create(
                company=company,
                deadline=deadline
            )

            for service in services_to_invoice:
                # Create an invoice item for each service.
                # The amount is set in the save() method of InvoiceItem.
                InvoiceItem.objects.create(
                    invoice=invoice,
                    service=service
                )
                # Mark the service as invoiced so it's not processed again.
                service.is_invoiced = True
                service.save()

            # Calculate and update the invoice total based on all invoice items.
            invoice.calculate_total()
            self.stdout.write(
                f"Created Invoice #{invoice.id} for {company.name} with total amount {invoice.total_amount} "
                f"and deadline {invoice.deadline.strftime('%Y-%m-%d %H:%M')}."
            )

        self.stdout.write("Invoice generation completed.")
