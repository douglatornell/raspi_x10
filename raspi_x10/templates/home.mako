<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>RaspPi-X10 Remote</title>

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/style.css">
  </head>

  <body>
    <div class="navbar navbar-default" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button class="navbar-toggle" type="button"
                  data-toggle="collapse" data-target="navbar-collapse">
            <span class="sr-only">Toggle Navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a href="#" class="navbar-brand">RaspPi-X10</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="row bottom-margin">
        <div class="col-xs-6 col-xs-offset-3 col-md-4 col-md-offset-0">
          <div class="btn-group-vertical">
            <button type="button" id="people-home" class="btn btn-info away-mode">People Home</button>
            <button type="button" id="away-mode" class="btn btn-default away-mode">Away Mode</button>
          </div>
        </div>
      </div>
      <div class="row" style="margin-bottom: 15px">
        <div class="col-xs-6 col-xs-offset-3 col-md-4 col-md-offset-0">
          <div class="btn-group-vertical">
            <button type="button" id="refresh-status" class="btn btn-warning">Refresh Status</button>
          </div>
        </div>
      </div>
    </div>

    <script src="//code.jquery.com/jquery.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    <script src="/static/web_remote.js"></script>
  </body>
</html>
