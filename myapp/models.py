

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.user.username} ({self.region})"


class Applicant(models.Model):
    application_id               = models.CharField(max_length=50,null=True, blank=True)
    program_key                  = models.CharField(max_length=50, null=True, blank=True)
    nd_title                     = models.CharField(max_length=512, null=True, blank=True)
    user_id                      = models.CharField(max_length=50, null=True, blank=True)
    first_name                   = models.CharField(max_length=100, null=True, blank=True)
    last_name                    = models.CharField(max_length=100, null=True, blank=True)
    email                        = models.EmailField(max_length=254, null=True, blank=True)
    nd_key                       = models.CharField(max_length=50, null=True, blank=True)
    company_id                   = models.CharField(max_length=50, null=True, blank=True)
    company_name                 = models.CharField(max_length=512, null=True, blank=True)
    country_at_registration      = models.CharField(max_length=100, null=True, blank=True)
    application_status           = models.CharField(max_length=100, null=True, blank=True)
    application_submitted_at     = models.DateTimeField(null=True, blank=True)
    application_created_at       = models.DateTimeField(null=True, blank=True)
    applicant_updated_at         = models.DateTimeField(null=True, blank=True)
    heard_about_program          = models.CharField(
                                      max_length=512,
                                      null=True,
                                      blank=True,
                                      verbose_name="How did you hear about this program?"
                                   )
    experience_years             = models.CharField(
                                      max_length=50,
                                      null=True,
                                      blank=True,
                                      verbose_name="How many years of professional experience do you have?"
                                   )
    terms_agreement              = models.CharField(
                                      max_length=50,
                                      null=True,
                                      blank=True,
                                      verbose_name=(
                                          "I confirm that the information I have provided above is accurate "
                                          "and I agree to the terms and conditions at https://udacity.com.legal"
                                      )
                                   )
    employer_name                = models.CharField(
                                      max_length=512,
                                      null=True,
                                      blank=True,
                                      verbose_name="If employed, what is the name of your employer?"
                                   )
    age                          = models.CharField(
                                      max_length=50,
                                      null=True,
                                      blank=True,
                                      verbose_name="Please confirm your age"
                                   )
    phone_number                 = models.CharField(
                                      max_length=50,
                                      null=True,
                                      blank=True,
                                      verbose_name="Please confirm your phone number"
                                   )
    nationality                  = models.CharField(
                                      max_length=100,
                                      null=True,
                                      blank=True,
                                      verbose_name="Please indicate your country of nationality"
                                   )
    region                       = models.CharField(
                                      max_length=100,
                                      null=True,
                                      blank=True,
                                      verbose_name="Please indicate your region in Ethiopia"
                                   )
    education_level              = models.CharField(
                                      max_length=512,
                                      null=True,
                                      blank=True,
                                      verbose_name="What is the highest level of education you have completed?"
                                   )
    education_institution        = models.CharField(
                                      max_length=512,
                                      null=True,
                                      blank=True,
                                      verbose_name="What is the name of your education institution"
                                   )
    employment_status            = models.CharField(
                                      max_length=100,
                                      null=True,
                                      blank=True,
                                      verbose_name="What is your current employment status?"
                                   )
    field_of_study               = models.CharField(
                                      max_length=100,
                                      null=True,
                                      blank=True,
                                      verbose_name="What is your field of study?"
                                   )
    gender                       = models.CharField(
                                      max_length=50,
                                      null=True,
                                      blank=True,
                                      verbose_name="What is your gender?"
                                   )
    primary_reason               = models.TextField(
                                      null=True,
                                      blank=True,
                                      verbose_name="What is your primary reason for enrolling in this program?"
                                   )

    def __str__(self):
        return f"{self.application_id} – {self.first_name} {self.last_name}"
