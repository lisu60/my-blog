from flask import Flask, request, url_for, render_template_string

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = False


@app.errorhandler(404)
def page_not_found(e):
    template = """
  <!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Murphy</title>

<link href="/static/css/bootstrap.min.css" rel="stylesheet">
<link href="/static/css/styles.css" rel="stylesheet">


</head>

<body>
	<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
		<a class="navbar-brand"  href="{0}">Home</a>
		<div class="container-fluid">
			
			<div class="navbar-header">
				<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#sidebar-collapse">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<ul class="user-menu">
					<li class="dropdown pull-right">

						<ul class="dropdown-menu" role="menu">
						</ul>
					</li>
				</ul>
			</div>
		</div>
	</nav>

	<div class="container main">
		<div class="row">

		</div>

		<div class="row">
			<div class="col-lg-12">
				<h1 class="page-header">Welcome! </h1>
			</div>
		</div>


		<div class="row">
			<div class="col-lg-12">
				<div class="panel panel-default">
					<div class="panel-body">
						<div class="col-md-12">
								<p style="font-size:2em;">
									- things will go wrong in any given situation, if you give them a chance," or more commonly, "whatever can go wrong, will go wrong." A number of variants on the rule have been formulated, as have several corollaries. 
								</p>
               			</div>
               			<div class="col-md-12">
								<p style="font-size:2em;">
									- If there's more than one way to do a job, and one of those ways will result in disaster, then somebody will do it that way.
								</p>
               			</div>
					</div>
				</div>
			</div>
		</div>


	</div>
	<center> <p style="font-size:2em;">&#169;</p></center>
	<script src="/static/js/jquery-1.11.1.min.js"></script>
	<script src="/static/js/bootstrap.min.js"></script>
</body>

</html>

""".format(request.url)
    return render_template_string(template), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')