# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

import babel

LANGUAGES = {u'afrikaans': 'af',
             u'arabic': 'ar',
             u'assamese': 'as',
             u'arabe': 'ar',
             u'english': 'en',
             u'esperanto': 'eo',
             u'spanish': 'es',
             u'espanol': 'es',
             u'some spanish': 'es',
             u'basque': 'eu',
             u'persian': 'fa',
             u'farsi': 'fa',
             u'finnish': 'fi',
             u'french': 'fr',
             u'francais': 'fr',
             u'some french': 'fr',
             u'fr': 'fr',
             u'gujarati': 'gu',
             u'hebrew': 'he',
             u'hindi': 'hi',
             u'croatian': 'hr',
             u'hungarian': 'hu',
             u'armenian': 'hy',
             u'indonesian': 'id',
             u'bahasa indonesia': 'id',
             u'bahasa': 'id',
             u'italian': 'it',
             u'italiano': 'it',
             u'japanese': 'ja',
             u'javanese': 'jv',
             u'khmer': 'km',
             u'kannada': 'kn',
             u'korean': 'ko',
             u'latin': 'la',
             u'luganda': 'lg',
             u'latvian': 'lv',
             u'malayalam': 'ml',
             u'marathi': 'mr',
             u'malay': 'ms',
             u'bahasa malaysia': 'ms',
             u'norwegian': 'nb',
             u'nepali': 'ne',
             u'dutch': 'nl',
             u'nederlands': 'nl',
             u'oriya': 'or',
             u'punjabi': 'pa',
             u'polish': 'pl',
             u'polski': 'pl',
             u'portuguese': 'pt',
             u'portugues': 'pt',
             u'brazilian portuguese': 'pt_BR',
             u'romanian': 'ro',
             u'russian': 'ru',
             u'sanskrit': 'sa',
             u'sinhala': 'si',
             u'slovak': 'sk',
             u'slovenian': 'sl',
             u'albanian': 'sq',
             u'serbian': 'sr',
             u'swedish': 'sv',
             u'swahili': 'sw',
             u'kiswahili': 'sw',
             u'tamil': 'ta',
             u'telugu': 'te',
             u'thai': 'th',
             u'tagalog': 'tl',
             u'filipino': 'tl',
             u'turkish': 'tr',
             u'ukrainian': 'uk',
             u'urdu': 'ur',
             u'vietnamese': 'vi',
             u'chinese': 'zh_Hans',
             u'mandarin': 'zh_Hans',
             u'cantonese': 'zh_Hans',
             u'mandarin chinese': 'zh_Hans',
             u'traditional chinese': 'zh_Hant',
             u'taiwanese': 'zh_Hans',
             u'chinese traditional': 'zh_Hant',
             u'german': 'de',
             u'anglais': 'en',
             u'bangla': 'bn',
             u'bengali': 'bn',
             u'englisch': 'en',
             u'en': 'en',
             u'ingles': 'en',
             u'indonesia': 'id',
             u'angielski': 'en',
             u'balinese': 'ban',
             u'sundanese': 'su',
             u'marwari': 'mwr',
             u'bhojpuri': 'bho',
             u'bosnian': 'bs',
             u'bulgarian': 'bg',
             u'catalan': 'ca',
             u'czech': 'cs',
             u'danish': 'da',
             u'de': 'de',
             u'deutsch': 'de',
             u'frances': 'fr',
             u'greek': 'el',
             u'lithuanian': 'lt',
             u'macedonian': 'mk',
             u'maithili': 'mai',
             u'mongolian': 'mn',
             u'newari': 'new',
             u'rajasthani': 'raj',
             u'aragonese': 'an',
             u'british english': 'en',
             u'burmese': 'my'} 


class Migration(DataMigration):

    def forwards(self, orm):
        """Migrate matching languages to user's UserProfile."""

        profiles = orm['users.UserProfile'].objects.all()
        for profile in profiles:
            common_set = profile.languages.filter(name__in=LANGUAGES)
            for language in common_set:
                orm['users.Language'].objects.get_or_create(
                    userprofile=profile, code=LANGUAGES[language.name])
        orm['groups.Language'].objects.all().delete()

    def backwards(self, orm):
        """Delete all the languages from the UserProfile of a user."""
        profiles = orm['users.UserProfile'].objects.all()
        available_languages = babel.Locale('en').languages

        for profile in profiles:
            lang_codes = profile.language_set.values_list('code', flat=True)
            user_languages = []
            for code in lang_codes:
                user_languages.append(available_languages[code])
            for language in user_languages:
                lang, created = orm['groups.Language'].objects.get_or_create(name=language.lower())
                profile.languages.add(lang)
        orm['users.Language'].objects.all().delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'groups.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'accepting_new_members': ('django.db.models.fields.CharField', [], {'default': "'by_request'", 'max_length': '10'}),
            'curator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'groups_curated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['users.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'functional_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irc_channel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '63', 'blank': 'True'}),
            'max_reminder': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'members_can_leave': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'wiki': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'groups.groupmembership': {
            'Meta': {'unique_together': "(('userprofile', 'group'),)", 'object_name': 'GroupMembership'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"})
        },
        'groups.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'groups.skill': {
            'Meta': {'ordering': "['name']", 'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'users.externalaccount': {
            'Meta': {'ordering': "['type']", 'unique_together': "(('identifier', 'type', 'user'),)", 'object_name': 'ExternalAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'privacy': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"})
        },
        'users.language': {
            'Meta': {'ordering': "['code']", 'unique_together': "(('code', 'userprofile'),)", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']"})
        },
        'users.usernameblacklist': {
            'Meta': {'ordering': "['value']", 'object_name': 'UsernameBlacklist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_regex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'users.userprofile': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'UserProfile', 'db_table': "'profile'"},
            'allows_community_sites': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allows_mozilla_sites': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'basket_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'date_mozillian': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_vouched': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'blank': 'True', 'through': "orm['groups.GroupMembership']", 'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ircname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '63', 'blank': 'True'}),
            'is_vouched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'blank': 'True', 'to': "orm['groups.Language']"}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'privacy_bio': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_city': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_country': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_date_mozillian': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_email': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_full_name': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_groups': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_ircname': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_languages': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_photo': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_region': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_skills': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_timezone': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_title': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'privacy_tshirt': ('mozillians.users.models.PrivacyField', [], {'default': '1'}),
            'privacy_vouched_by': ('mozillians.users.models.PrivacyField', [], {'default': '3'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'blank': 'True', 'to': "orm['groups.Skill']"}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '70', 'blank': 'True'}),
            'tshirt': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'vouched_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vouchees'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['users.UserProfile']", 'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['users']
    symmetrical = True
