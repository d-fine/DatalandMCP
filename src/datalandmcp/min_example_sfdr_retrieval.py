from datalandmcp.dataland_client import PRODUCTION_INSTANCE, DatalandClient
DatalandClient.set_global_client(PRODUCTION_INSTANCE.client)
client=DatalandClient.get_global_client()

company_name = "Adidas"
# Get company id by name
company = client.company_api.get_companies(search_string=company_name, data_types=["sfdr"])[0]
company_id = company.company_id
# Fetch SFDR data
sfdr_data = client.sfdr_api.get_all_company_sfdr_data(company_id=company_id, reporting_period="2024")[0].data
# Print Scope 1 emissions
print(f"Scope 1 emissions for {company.company_name}: {sfdr_data.environmental.greenhouse_gas_emissions.scope1_ghg_emissions_in_tonnes.value} tonnes CO2e")
