"WTForms for wgm_search"

from wtforms import Form, BooleanField, TextField, SelectField, SubmitField, validators, ValidationError
import pygeodb

def zip_exists(message=None):
    "Validates that a zip exists"

    def _zip_exists(form, field):
        z = field.data
        if not z in pygeodb.geodata['DE']:
            raise ValidationError(message)

    return _zip_exists

distance_choices = [(5, "5km"), (10, "10km"), (15, "15km"), (20, "20km"), (30, "30km"), (40, "40km"), (50, "50km")]
distance_values = [distance[0] for distance in distance_choices]
class SearchForm(Form):
    "Basic search form, containing only the ZIP and a submit button"

    zip     = TextField(u'Postleitzahl', [validators.Length(min=5, max=5, message=u'Postleitzahlen muessen 5 Ziffern enthalten'),
        zip_exists(u'Postleitzahl existiert nicht! Bitte geben Sie eine existierende PLZ ein.')])
    submit  = SubmitField(u'Search')

class CitySearchForm(SearchForm):
    "Form for city search, extending SearchForm, containing, ZIP and city"

    zip     = TextField(u'Postleitzahl', [validators.Length(min=3, max=5, message=u'Postleitzahlen muessen %(min) Ziffern enthalten, maximal %(max)')])
    city    = TextField(u'Stadt', [validators.Length(min=2, max=255, message=u'Der St&auml;dtenamen muss mindestens %(min) Zeichen lang sein')])

class DistanceSearchForm(SearchForm):
    "Form for distance searches, extending SearchForm by distance select field"

    distance    = SelectField(u'Entfernung', coerce=int, choices=distance_choices, validators=[validators.AnyOf(values=distance_values, message=u'Please select one of the given options')])
