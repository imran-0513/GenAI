from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import pandas as pd

key = "127a6d9b2e05462883d9885566908b8a"
endpoint = "https://analyzepdfs.cognitiveservices.azure.com/"

fileUrl = "https://github.com/MicrosoftLearning/mslearn-ai-document-intelligence/blob/main/Labfiles/01-prebuild-models/sample-invoice/sample-invoice.pdf?raw=true"

fileLocale = "en-US"
fileModelID = 'prebuilt-invoice'

credential = AzureKeyCredential(key)
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)

poller = document_analysis_client.begin_analyze_document_from_url(fileModelID, fileUrl, locale=fileLocale)
receipts = poller.result()

# Initialize lists to store extracted information
vendor_names = []
customer_names = []
invoice_dates = []
addresses = []

for id, receipt in enumerate(receipts.documents):
    vendor_names.append(receipt.fields.get("VendorName").value)
    customer_names.append(receipt.fields.get("CustomerName").value)
    invoice_dates.append(receipt.fields.get("InvoiceDate").value)

    # Extract common address details:
    billing_address = receipt.fields.get("BillingAddress").value
    street_address = billing_address.street_address if billing_address.street_address else ''
    city = billing_address.city if billing_address.city else ''
    state = billing_address.state if billing_address.state else ''
    postal_code = billing_address.postal_code if billing_address.postal_code else ''
    country = billing_address.country_region if billing_address.country_region else ''
    addresses.append(f"{street_address}, {city}, {state}, {postal_code}, {country}")

# Creating a DataFrame
data = {
    "Vendor Name": vendor_names,
    "Customer Name": customer_names,
    "Invoice Date": invoice_dates,
    "Address": addresses
}

df = pd.DataFrame(data)

# Print the DataFrame
print(df)
