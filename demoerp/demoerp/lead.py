import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_project

# @frappe.whitelist()
# def validate(self, method):
#     for d in self.items:
#         d.bom_no = None

# @frappe.whitelist()
# def auto_project_creation_on_submit(doc, method):
#     project_make = make_project(doc)
#     project_make.custom_poc_person_name = doc.custom_person_name
#     project_make.custom_poc_mobile_no = doc.custom_another_mobile_no
#     project_make.save()
#     create_subsidy(project_make)
#     update_opportunity(doc)

# def create_subsidy(project_make):
#     doc = project_make
#     if doc.custom_type_of_case == "Subsidy":
#         discomDoc = frappe.new_doc('Discom')
#         discomDoc.project_name = doc.name
#         discomDoc.sales_order = doc.sales_order
#         discomDoc.customer_name = doc.customer
#         discomDoc.save()

#         subsidyDoc = frappe.new_doc('Subsidy')
#         subsidyDoc.project_name = doc.name
#         subsidyDoc.sales_order = doc.sales_order
#         subsidyDoc.customer_name = doc.customer
#         subsidyDoc.save()
                       
#     elif doc.custom_type_of_case == "Non Subsidy":
#         discomDoc = frappe.new_doc('Discom')
#         discomDoc.project_name = doc.name
#         discomDoc.sales_order = doc.sales_order
#         discomDoc.customer_name = doc.customer
#         discomDoc.save()

# def update_opportunity(doc):
#     if doc.items[0].quotation_item:
#         qi = frappe.get_doc("Quotation Item", doc.items[0].quotation_item)
#         if qi.prevdoc_docname and qi.prevdoc_doctype == "Opportunity":
#             op = frappe.get_doc(qi.prevdoc_doctype, qi.prevdoc_docname)
#             op.db_set("opportunity_amount", doc.rounded_total, update_modified=False)

@frappe.whitelist()
def create_opportunity_from_lead(lead_name):
    lead = frappe.get_doc("Lead", lead_name)
    if lead.custom_lead_status == "Interested":
        opportunity = frappe.new_doc("Opportunity")
        opportunity.lead = lead.name
        opportunity.customer_name = lead.lead_name
        opportunity.contact_email = lead.email_id
        opportunity.contact_mobile = lead.mobile_no
        opportunity.opportunity_from = "Lead"
        opportunity.save()
        frappe.msgprint(f"Opportunity {opportunity.name} created from Lead {lead.name}")

def lead_validate(doc, method):
    if doc.custom_lead_status == "Interested":
        create_opportunity_from_lead(doc.name)
