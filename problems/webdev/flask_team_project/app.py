from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
import random

app = Flask(__name__)
app.debug = True
import meetup.api
app.config['SECRET_KEY'] = 'foobar'

toolbar = DebugToolbarExtension(app)

def get_names():
    client = meetup.api.Client("api key")

    rsvps = client.GetRsvps(event_id='244121900', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    foo = {}
    for member in members.results:
        try:
            foo[member['name']] = member['photo']['thumb_link']
        except:
            pass # ignore those who do not have a complete profile
    return foo

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

member_rsvps = get_names()

@app.route('/rsvps')
def rsvps():
    return render_template('rsvps.html', rsvps=member_rsvps)


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    results = request.form.to_dict()
    results = {key: int('0' + value) for key, value in results.items()}
    members = list(results.items())
    random.shuffle(members)
    teams = chunks(members, 4)
    teams = [dict(team) for team in teams]
    print(teams)



    return render_template('teams.html', teams=teams, img=member_rsvps)

if __name__ == '__main__':
    app.run(debug=True)
