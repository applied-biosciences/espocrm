# PDF branding foundation

Sales Pack is not installed. These three HTML files are design specifications and future template-adapter inputs only. Stage 3 does not create a second invoice, PO, financial posting or PDF engine.

Live static previews:
- http://localhost:8080/client/custom/branding/pdf/quotation.html
- http://localhost:8080/client/custom/branding/pdf/invoice.html
- http://localhost:8080/client/custom/branding/pdf/purchase-order.html

Each defines A4 paper, the supplied logo, NuriVoyage/Nuri's Travel identity, royal-blue headings/table header, a gold rule, document number/date block, customer/supplier block, line-item columns, total and terms/footer. Browser preview canvas is cyan; print CSS uses white paper. Placeholder values are deliberately unresolved. These are not valid invoices or purchase orders and contain no real company legal/bank details.

Future integration hook: pass an approved native Sales Pack or Espo template renderer a record-to-placeholder adapter mapping DOCUMENT_NUMBER, DD/MM/YYYY, CUSTOMER_NAME/SUPPLIER_NAME, approved party details, line description/quantity/unit price/total, currency/total, approved terms and company contacts. Add row iteration using that renderer's syntax at integration time. Preserve financial ACL before resolving supplier costs. Never expose internal purchase costs in a customer document.

Human review checks the stored design specification/previews. Actual generated-PDF behaviour remains pending installation/integration of the appropriate functionality; no claim of generated PDF testing is made in Stage 3.
