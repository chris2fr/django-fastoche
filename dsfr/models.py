import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".jpg", ".jpeg", ".png", ".svg"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension.")


class DsfrConfig(models.Model):
    A11Y_CHOICES = [
        ("FULL", _("fully")),
        ("PART", _("partially")),
        ("NOT", _("not")),
    ]

    # Site
    site_title = models.CharField(
        "Titre du site", max_length=200, default="Titre du site", blank=True
    )
    site_tagline = models.CharField(
        "Sous-titre du site", max_length=200, default="Sous-titre du site", blank=True
    )
    notice = models.TextField(
        "Bandeau d’information importante",
        default="",
        blank=True,
    )

    # Header
    header_brand = models.CharField(
        "Institution (en-tête)",
        max_length=200,
        default="République française",
        blank=True,
    )
    header_brand_html = models.CharField(
        "Institution avec césure (en-tête)",
        max_length=200,
        default="République<br />française",
        blank=True,
    )
    beta_tag = models.BooleanField("Afficher la mention BETA à côté du titre", default=False)  # type: ignore

    # Footer
    footer_brand = models.CharField(
        "Institution (pied)", max_length=200, default="République française", blank=True
    )
    footer_brand_html = models.CharField(
        "Institution avec césure (pied)",
        max_length=200,
        default="République<br />française",
        blank=True,
    )
    footer_description = models.TextField("Description", default="", blank=True)

    newsletter_description = models.TextField(
        "Description de la newsletter", default="", blank=True
    )

    newsletter_url = models.URLField(
        "URL d’inscription à la newsletter",
        default="",
        blank=True,
    )

    # Operator logo
    operator_logo_file = models.FileField(
        "Logo opérateur",
        upload_to="logos",
        blank=True,
        null=True,
        validators=[validate_image_extension],
    )
    operator_logo_alt = models.CharField(
        "Alternative textuelle du logo",
        max_length=200,
        blank=True,
        help_text="Doit impérativement contenir le texte présent dans l’image.",
    )
    operator_logo_width = models.DecimalField(
        "Largeur (em)",
        max_digits=3,
        decimal_places=1,
        null=True,
        default="0.0",
        help_text="""À ajuster en fonction de la largeur du logo.
        Exemple pour un logo vertical: 3.5, Exemple pour un logo horizontal: 8.""",
    )

    # Advanced
    mourning = models.BooleanField("Mise en berne", default=False)  # type: ignore

    accessibility_status = models.CharField(
        "Statut de conformité de l’accessibilité",
        max_length=4,
        choices=A11Y_CHOICES,
        default="NOT",
    )

    class Meta:
        verbose_name = "Configuration"

    def __str__(self):
        return f"Configuration du site : {self.site_title}"

    def save(self, *args, **kwargs):
        if not self.pk and DsfrConfig.objects.exists():
            raise ValidationError("There can be only one DsfrBaseSettings instance")
        return super(DsfrConfig, self).save(*args, **kwargs)

    def social_media(self):
        return self.dsfrsocialmedia_set.all()


class DsfrSocialMedia(models.Model):
    site_config = models.ForeignKey(DsfrConfig, on_delete=models.CASCADE, null=True)
    title = models.CharField(_("Title"), max_length=200, default="", blank=True)

    url = models.URLField(
        _("URL"),
        default="",
        blank=True,
    )
    icon_class = models.CharField(
        _("Icon class"), max_length=200, default="", blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _("Social media")
        verbose_name_plural = _("Social medias")
