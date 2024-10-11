from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Car Rental Admin",
    "SITE_HEADER": "Car Rental Admin",
    "SITE_URL": "https://google.com",
    "SITE_ICON": {
        "light": lambda request: static("admin/img/logo.png"),  # light mode
        "dark": lambda request: static("admin/img/logo.png"),  # dark mode
    },
    # "SITE_LOGO": {
    #     "light": lambda request: static("admin/img/favicon.svg"),  # light mode
    #     "dark": lambda request: static("admin/img/favicon.svg"),  # dark mode
    # },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "ENVIRONMENT": "apps.common.views.environment_callback",
    # "DASHBOARD_CALLBACK": "apps.common.dashboard.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("admin/img/logo.png"),
    },
    "STYLES": [
        lambda request: static("assets/css/main.css"),
    ],
    "SCRIPTS": [
        lambda request: static("assets/js/admin.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "uz": "🇺🇿",
    #             "ru": "🇷🇺",
    #             "en": "🇬🇧",
    #         },
    #     },
    # },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                    },
                ],
            },
            # Users
            {
                "title": _("Users"),
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            # Driver Licence
            {
                "title": ("Driver Licence"),
                "separator": True,
                "items": [
                    {
                        "title": ("Driver Licence"),
                        "icon": "assignment",
                        "link": reverse_lazy("admin:users_driverlicence_changelist"),
                    }
                ]
            },
            # Brand
            {
                "title": _("Brand"),
                "separator": True,
                "items": [
                    {
                        "title": _("Brand"),
                        "icon": "home_repair_service",
                        "link": reverse_lazy("admin:car_brand_changelist"),
                    },
                ]
            },
            # Car
            {
                "title": _("Car"),
                "separator": True,
                "items": [
                    {
                        "title": _("Car"),
                        "icon": "home_repair_service",
                        "link": reverse_lazy("admin:car_car_changelist"),
                    },
                ]
            },
            
            # Common
            # {
            #     "title": _("Common"),
            #     "separator": True,
            #     "items": [
            #         {
            #             "title": _("FAQ"),
            #             "icon": "help_center", 
            #             "link": reverse_lazy("admin:common_faq_changelist"), 
            #         },
            #         {
            #             "title": _("Plumber Application"),
            #             "icon": "engineering",
            #             "link": reverse_lazy("admin:common_plumberapplicationform_changelist"),
            #         },
            #         {
            #             "title": _("Static Page"),
            #             "icon": "pages",
            #             "link": reverse_lazy("admin:common_staticpage_changelist"),
            #         },
            #     ]
            # },
        ],
    },
}
