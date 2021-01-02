from flask import Flask, make_response, send_file
from flask_restx import Resource, Api

import io
import csv
import zipfile

app = Flask(__name__)
api = Api(app)

@api.route('/download')
class HelloWorld(Resource):
    def get(self):

        files = []
        si = io.StringIO()
        cw = csv.writer(si)
        csvList = ["1", "0", "2"]
        cw.writerows(csvList)

        si.seek(0)
        files.append(si)

        zipped_file = io.BytesIO()

        with zipfile.ZipFile(zipped_file, 'w') as zipper:
            for i, csv_file in enumerate(files):
                csv_file.seek(0)
                zipper.writestr("export.csv", csv_file.read())

        zipped_file.seek(0)
        response = make_response(send_file(zipped_file, attachment_filename='export.zip', as_attachment=True))
        response.headers["sdmx-attributes"] = "some value"
        return response


        # return send_file(zipped_file, attachment_filename='export.zip', as_attachment=True)

        # output = make_response(si.getvalue())
        # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        # output.headers["Content-type"] = "text/csv"
        # return output

if __name__ == '__main__':
    app.run(debug=True)