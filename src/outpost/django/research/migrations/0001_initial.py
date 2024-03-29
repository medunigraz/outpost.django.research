# Generated by Django 2.2.28 on 2024-02-12 14:56

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bidding",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("short", models.TextField()),
                ("description", models.TextField()),
                ("mode", models.CharField(blank=True, max_length=256, null=True)),
                ("url", models.URLField(blank=True, null=True)),
                ("running", models.BooleanField()),
                ("start", models.DateTimeField()),
            ],
            options={
                "db_table": "research_bidding",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="BiddingDeadline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deadline", models.DateTimeField()),
                ("time", models.CharField(blank=True, max_length=16, null=True)),
                ("comment", models.TextField()),
            ],
            options={
                "db_table": "research_biddingdeadline",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="BiddingEndowment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("information", models.TextField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=20)),
                ("currency", models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                "db_table": "research_biddingendowment",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Classification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
                ("level", models.PositiveSmallIntegerField()),
            ],
            options={
                "db_table": "research_classification",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
                ("iso", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_country",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_education",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Expertise",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_expertise",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Field",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
                ("short", models.CharField(blank=True, max_length=12, null=True)),
            ],
            options={
                "db_table": "research_field",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Funder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("street", models.CharField(blank=True, max_length=256, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=32, null=True)),
                ("city", models.CharField(blank=True, max_length=256, null=True)),
                ("url", models.CharField(blank=True, max_length=256, null=True)),
                ("telephone", models.CharField(blank=True, max_length=256, null=True)),
                ("email", models.CharField(blank=True, max_length=256, null=True)),
                ("patron", models.BooleanField()),
                ("patron_peer_review", models.BooleanField()),
                ("patron_associate_professor", models.BooleanField()),
            ],
            options={
                "db_table": "research_funder",
                "permissions": (
                    ("view_funder_non_patron", "View funders that are not a patron"),
                ),
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="FunderCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "db_table": "research_fundercategory",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="FunderTypeIntellectualCapitalAccounting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_fundertypeintellectualcapitalaccounting",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="FunderTypeStatisticsAustria",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_fundertypestatisticsaustria",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Knowledge",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_knowledge",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("iso", models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                "db_table": "research_language",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short", models.CharField(blank=True, max_length=128, null=True)),
                ("street", models.CharField(blank=True, max_length=128, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=128, null=True)),
                ("city", models.CharField(blank=True, max_length=128, null=True)),
                ("url", models.CharField(blank=True, max_length=128, null=True)),
                ("telephone", models.CharField(blank=True, max_length=128, null=True)),
                ("email", models.CharField(blank=True, max_length=128, null=True)),
                ("information", models.TextField()),
            ],
            options={
                "db_table": "research_partner",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PartnerTypeIntellectualCapitalAccounting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_partnertypeintellectualcapitalaccounting",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("active", models.BooleanField()),
            ],
            options={
                "db_table": "research_program",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("short", models.CharField(blank=True, max_length=256, null=True)),
                ("title", django.contrib.postgres.fields.hstore.HStoreField()),
                ("url", models.URLField(blank=True, null=True)),
                ("abstract", django.contrib.postgres.fields.hstore.HStoreField()),
                ("begin_planned", models.DateTimeField(blank=True, null=True)),
                ("begin_effective", models.DateTimeField(blank=True, null=True)),
                ("end_planned", models.DateTimeField(blank=True, null=True)),
                ("end_effective", models.DateTimeField(blank=True, null=True)),
                ("assignment", models.DateTimeField(blank=True, null=True)),
                ("subprogram", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "research_project",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("third_party_funding_policy", models.BooleanField()),
            ],
            options={
                "db_table": "research_projectcategory",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "db_table": "research_projectevent",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectGrant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "db_table": "research_projectgrant",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectPartnerFunction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "db_table": "research_projectpartnerfunction",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectResearch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "db_table": "research_projectresearch",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("public", models.BooleanField()),
            ],
            options={
                "db_table": "research_projectstatus",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectStudy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
                ("active", models.BooleanField()),
            ],
            options={
                "db_table": "research_projectstudy",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("public", models.BooleanField()),
            ],
            options={
                "db_table": "research_projecttype",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Publication",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "authors",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=256), size=None
                    ),
                ),
                ("year", models.PositiveSmallIntegerField()),
                ("source", models.TextField()),
                ("sci", models.CharField(blank=True, max_length=128, null=True)),
                ("pubmed", models.CharField(blank=True, max_length=128, null=True)),
                ("doi", models.CharField(blank=True, max_length=128, null=True)),
                ("pmc", models.CharField(blank=True, max_length=128, null=True)),
                ("abstract", models.TextField(blank=True, null=True)),
                ("imported", models.DateTimeField()),
                ("journal", models.TextField(blank=True, null=True)),
                ("issn", models.CharField(blank=True, max_length=20, null=True)),
                ("collection_publisher", models.TextField(blank=True, null=True)),
                ("collection_title", models.TextField(blank=True, null=True)),
                ("edition", models.CharField(blank=True, max_length=50, null=True)),
                ("university", models.TextField()),
                ("case_report", models.BooleanField(null=True)),
                ("impactfactor", models.FloatField()),
                ("impactfactor_year", models.PositiveSmallIntegerField()),
                ("impactfactor_norm", models.FloatField()),
                ("impactfactor_norm_year", models.PositiveSmallIntegerField()),
                ("impactfactor_norm_category", models.TextField()),
                ("impactfactor_norm_super", models.FloatField()),
                ("impactfactor_norm_super_year", models.PositiveSmallIntegerField()),
                ("impactfactor_norm_super_category", models.TextField()),
                ("citations", models.BooleanField(null=True)),
                ("conference_name", models.BooleanField(null=True)),
                ("conference_place", models.BooleanField(null=True)),
                ("conference_international", models.BooleanField(null=True)),
                ("scientific_event", models.BooleanField(null=True)),
                ("invited_lecture", models.BooleanField(null=True)),
                ("keynote_speaker", models.BooleanField(null=True)),
                ("selected_presentation", models.BooleanField(null=True)),
                ("biobank_use", models.BooleanField(null=True)),
                ("bmf_use", models.BooleanField(null=True)),
                ("zmf_use", models.BooleanField(null=True)),
                ("local_affiliation", models.BooleanField(null=True)),
            ],
            options={
                "db_table": "research_publication",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PublicationAuthorship",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_publicationauthorship",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PublicationCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_publicationcategory",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PublicationDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_publicationdocument",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PublicationOrganization",
            fields=[
                (
                    "id",
                    models.CharField(max_length=256, primary_key=True, serialize=False),
                ),
                ("assigned", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "research_publicationorganization",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ResearchType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                "db_table": "research_research_type",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoProjectStatus",
            fields=[
                (
                    "id",
                    models.OneToOneField(
                        db_column="id",
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to="research.ProjectStatus",
                    ),
                ),
                ("public", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="DjangoProjectType",
            fields=[
                (
                    "id",
                    models.OneToOneField(
                        db_column="id",
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        related_name="+",
                        serialize=False,
                        to="research.ProjectType",
                    ),
                ),
                ("public", models.BooleanField(default=False)),
            ],
        ),
    ]
