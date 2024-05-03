
import frappe
from frappe import _
from frappe.utils import (
	escape_html
)

@frappe.whitelist(allow_guest=True)
def sign_up(email: str, full_name: str, redirect_to: str) -> tuple[int, str]:

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)

		# from frappe.utils import random_string
		password = str(escape_html(full_name) + "@123")
		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": escape_html(full_name),
				"enabled": 1,
				"new_password": password,
				"user_type": "Website User",
			}
		)
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()

		# set default signup role as per Portal Settings
		default_role = frappe.db.get_single_value("Portal Settings", "default_role")
		if default_role:
			user.add_roles(default_role)
			user.add_roles("Trial")

		if redirect_to:
			frappe.cache.hset("redirect_after_login", user.name, redirect_to)

		if user.flags.email_sent:
			return 1, _("Please check your email for verification")
		else:
			message = " Please Login with Email, Password  <br> Your Newly Created Password : <b>" + password +"</b>"
			return 2, _(message)