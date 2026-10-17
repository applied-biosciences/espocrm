# NuriVoyage Stage 8 Supplier and Product Catalogue

Stage 8 provides a local catalogue for supplier contacts and reusable travel products. Suppliers support airline, hotel, transfer, visa and other categories. Products carry a supplier, service type, destination, supplier product code, supplier cost, selling price, validity dates and active status.

Airline and hotel rows can be imported from CSV with `scripts/local import-catalogue FILE.csv`. Required columns are `supplierName,supplierCategory,productName,productType,destination,supplierCost,sellingPrice`; optional columns include `supplierCode,contactName,website,supplierProductCode,currency,validFrom,validTo`. Set `NURIVOYAGE_DRY_RUN=1` to validate without writing. No live supplier feeds or AWS deployment are included.
