from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient ## doc analysis

key = "127a6d9b2e05462883d9885566908b8a"
endpoint = "https://analyzepdfs.cognitiveservices.azure.com/"

fileUrl="https://github.com/MicrosoftLearning/mslearn-ai-document-intelligence/blob/main/Labfiles/01-prebuild-models/sample-invoice/sample-invoice.pdf?raw=true"

fileLocale="en-US"
fileModelID = 'prebuilt-invoice'

credential= AzureKeyCredential(key)
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint,credential=credential)

poller = document_analysis_client.begin_analyze_document_from_url(fileModelID,fileUrl,locale=fileLocale)
receipts = poller.result()

for id,receipt in enumerate(receipts.documents):
    # print(receipt.fields.keys())
    print("\nVendor Name:",receipt.fields.get("VendorName").value)
    print("\nCustomer Name:",receipt.fields.get("CustomerName").value)
    print("\nInvoice Date:",receipt.fields.get("InvoiceDate").value)
    # print("\nBilling Adress:",receipt.fields.get("BillingAddress").value)
    billing_address = receipt.fields.get("BillingAddress").value
    # print(billing_address)

    ## Extract common address details:
    street_address = billing_address.street_address if billing_address.street_address else ''
    city = billing_address.city if billing_address.city else ''
    state = billing_address.state if billing_address.state else ''
    postal_code = billing_address.postal_code if billing_address.postal_code else ''
    country = billing_address.country_region if billing_address.country_region else ''

    # Display extracted address details
    formatted_billing_address = f"""
    Billing Address:
        Street Address: {street_address}
        City: {city}
        State: {state}
        Postal Code: {postal_code}
        Country: {country}
    """

    print(formatted_billing_address)

    ### saving all those information in dataframe format
    import pandas as pd

    data = {
        "Field": ["Vendor Name", "Customer Name", "Invoice Date", "Address"],
        "Value": [receipt.fields.get("VendorName").value, receipt.fields.get("CustomerName").value,
                  receipt.fields.get("InvoiceDate").value, f"{street_address}, {city}, {state}, {postal_code}, {country}"]
        }
    

    df = pd.DataFrame(data)

    # Print the DataFrame
    print(df)



