from flask import Flask, render_template, send_file, url_for, request, flash
import model


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aboba1488'


@app.route('/')
def index():
    return render_template('index.html', class1='active', class2='', class3='', class4='')


@app.route('/report', methods=['POST'])
def report():
    # print(request.form['operator'])
    file = model.get_report(int(request.form['operator']))
    # if file:
    #     return send_file(file, as_attachment=True)
    flash('Ошибка формирования отчёта', category='error')
    return render_template('index.html', class1='active', class2='')


@app.route('/clever_cam', methods=['GET', 'POST'])
def clever_cam():
    if request.method == 'POST':
        entered_data = [request.form['pid'], request.form['cam'],
                        request.form['date'], request.form['start_time'], request.form['end_time']]
        result = model.get_cc_count(request.form['pid'], request.form['cam'],
                                    request.form['date'], request.form['start_time'], request.form['end_time'])
        return render_template('clever_cam.html', class1='', class2='active', entered_data=entered_data,  result=result)
    entered_data = ['', '', '', '', '']
    result = ['', '']
    return render_template('clever_cam.html', class1='', class2='active', entered_data=entered_data,  result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
