from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

import json
import os.path

from application.extensions import db
from application.models import LocalAuthority

viability = Blueprint('viability', __name__, template_folder='templates', url_prefix='/viability')


@viability.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return redirect(url_for('viability.local_authorities', local_authority=request.form['local-authority-select']))

    return render_template('/viability-index.html', localauthorities=LocalAuthority.query.all())

@viability.route('/local-authority/<local_authority>')
def local_authorities(local_authority):
    la = LocalAuthority.query.get(local_authority)
    return render_template('/la-viability-assessments.html', localauthority=la)


# =====================================================
# Routes for the (incomplete) viability summary journey
# =====================================================

@viability.route('/create-summary')
def start():
    return render_template('v-start-page.html')


@viability.route('/create-summary/select-local-authority', methods=['GET', 'POST'])
def local_authority():
    datafile = "application/data/localauthorities.json"
    if os.path.isfile(datafile):
        with open(datafile) as data_file:
            localauthorities = json.load(data_file)
    return render_template('v-local-authority.html', localauthorities=localauthorities['authorities'])


@viability.route('/create-summary/report-details')
def report_details():
    return render_template('v-report-details.html')


@viability.route('/create-summary/question')
def question():
    return render_template('v-question.html')


@viability.route('/create-summary/check-your-answers')
def check():
    return render_template('v-check-your-answers.html')


@viability.route('/create-summary/complete')
def complete():
    return render_template('v-complete.html')
