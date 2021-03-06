/*
** Annotator v1.2.10
** https://github.com/okfn/annotator/
**
** Copyright 2015, the Annotator project contributors.
** Dual licensed under the MIT and GPLv3 licenses.
** https://github.com/okfn/annotator/blob/master/LICENSE
**
** Built at: 2015-02-26 03:26:47Z
 */

// Generated by CoffeeScript 1.6.3
var singleton_store;
(function () {
  var __bind = function (fn, me) { return function () { return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function (child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __indexOf = [].indexOf || function (item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  Annotator.Plugin.Store = (function (_super) {
    __extends(Store, _super);

    Store.prototype.events = {
      'annotationCreated': 'annotationCreated',
      'annotationDeleted': 'annotationDeleted',
      'annotationUpdated': 'annotationUpdated'
    };

    Store.prototype.options = {
      annotationData: {},
      emulateHTTP: false,
      loadFromSearch: false,
      prefix: '/store',
      urls: {
        create: '/annotations/:resumeId/',
        read: '/annotations/:resumeId/:id',
        update: '/annotations/:resumeId/:id',
        destroy: '/annotations/:resumeId/:id',
        search: '/search/:resumeId/'
      }
    };

    function Store(element, options) {
      this._onError = __bind(this._onError, this);
      this._onLoadAnnotationsFromSearch = __bind(this._onLoadAnnotationsFromSearch, this);
      this._onLoadAnnotations = __bind(this._onLoadAnnotations, this);
      this._getAnnotations = __bind(this._getAnnotations, this);
      Store.__super__.constructor.apply(this, arguments);
      this.annotations = [];
    }

    Store.prototype.pluginInit = function () {
      if (!Annotator.supported()) {
        return;
      }
      if (this.annotator.plugins.Auth) {
        return this.annotator.plugins.Auth.withToken(this._getAnnotations);
      } else {
        return this._getAnnotations();
      }
    };

    Store.prototype._getAnnotations = function () {
      // this.options.loadFromSearch = true;
      if (this.options.loadFromSearch) {
        return this.loadAnnotationsFromSearch(this.options.loadFromSearch);
      } else {
        return this.loadAnnotations();
      }
    };

    Store.prototype.annotationCreated = function (annotation) {

      var _this = this;
      if (__indexOf.call(this.annotations, annotation) < 0) {
        this.registerAnnotation(annotation);
        return this._apiRequest('create', annotation, function (data) {
          if (data.id == null) {
            console.warn(Annotator._t("Warning: No ID returned from server for annotation "), annotation);
          }
          $("#next").prop('disabled', false);
          currerent_resume_id = localStorage.getItem("currentResumeId");
          annotator_history = localStorage.getItem('history') || {};
          if (annotator_history[currerent_resume_id]) {
            annotator_history[currerent_resume_id] += 1;
          } else {
            annotator_history[currerent_resume_id] = 1;
          }
          localStorage.setItem('history', annotator_history);

          return _this.updateAnnotation(annotation, data);
        });
      } else {
        return this.updateAnnotation(annotation, {});
      }
    };

    Store.prototype.annotationUpdated = function (annotation) {
      var _this = this;
      if (__indexOf.call(this.annotations, annotation) >= 0) {
        return this._apiRequest('update', annotation, (function (data) {
          return _this.updateAnnotation(annotation, data);
        }));
      }
    };

    Store.prototype.annotationDeleted = function (annotation) {
      var _this = this;
      if (__indexOf.call(this.annotations, annotation) >= 0) {
        return this._apiRequest('destroy', annotation, (function () {
          currerent_resume_id = localStorage.getItem("currentResumeId");
          annotator_history = localStorage.getItem('history') || {};
          if (annotator_history[currerent_resume_id]) {
            annotator_history[currerent_resume_id] = annotator_history[currerent_resume_id] - 1;
          }
          if (annotator_history[currerent_resume_id] && annotator_history[currerent_resume_id] < 1) {
            annotator_history[currerent_resume_id] = 0;
          }
          localStorage.setItem('history', annotator_history);

          return _this.unregisterAnnotation(annotation);
        }));
      }
    };

    Store.prototype.registerAnnotation = function (annotation) {
      return this.annotations.push(annotation);
    };

    Store.prototype.unregisterAnnotation = function (annotation) {
      return this.annotations.splice(this.annotations.indexOf(annotation), 1);
    };

    Store.prototype.updateAnnotation = function (annotation, data) {
      if (__indexOf.call(this.annotations, annotation) < 0) {
        console.error(Annotator._t("Trying to update unregistered annotation!"));
      } else {
        $.extend(annotation, data);
      }

      var resumeId = localStorage.getItem('currentResumeId');
      var resumeOrder = JSON.parse(localStorage.getItem('resumeOrder'));
      if (resumeOrder.indexOf(resumeId) > 0) {
        $("#prev").prop('disabled', false);
      } else {
        $("#prev").prop('disabled', true);
      }
      return $(annotation.highlights).data('annotation', annotation);
    };

    Store.prototype.loadAnnotations = function (resumeId) {
      var currentResumeId = localStorage.getItem('currentResumeId');
      var self = this;
      singleton_store = self;
      var username = localStorage.getItem('userName');
      var resumeGetDataUrl;
      if (resumeId && resumeId != "undefined" && resumeId !== "next") {
        resumeGetDataUrl = 'http://192.168.3.12/resume/data/' + resumeId;
      } else {
        if (currentResumeId && currentResumeId != "undefined" && resumeId !== "next") {
          resumeGetDataUrl = 'http://192.168.3.12/resume/data/' + currentResumeId;
        } else {
          resumeGetDataUrl = 'http://192.168.3.12/resume/data';
        }

      }
      $.ajax({
        url: resumeGetDataUrl,
        type: 'GET',
        headers: {
          "username": username,
          "content-type": 'application/json'
        },
        dataType: 'json',
        success: function (data) {
          if (data.resume === 'All resumes are annotated') {
            alert(data.resume + '. Thanks for your participation');
            window.location.href = 'http://192.168.3.12/';
            return;
          }
          $("#annotatorjs p").html(data.resume);
          var resumeId = data.resumeId;
          var resumeOrderArrayString = localStorage.getItem('resumeOrder');
          var resumeOrder = resumeOrderArrayString ? JSON.parse(localStorage.getItem('resumeOrder')) : [];
          if (resumeOrder.indexOf(resumeId) < 0) {
            resumeOrder.push(resumeId);
            localStorage.setItem('resumeOrder', JSON.stringify(resumeOrder));
          }
          var current = localStorage.getItem('currentResumeId');
          if (resumeOrder.indexOf(resumeId) > 0) {
            $("#prev").prop('disabled', false);
          } else {
            $("#prev").prop('disabled', true);
          }
          localStorage.setItem('currentResumeId', resumeId);
          var approverName = data.approverName;

          annotation_history = localStorage.getItem('history') || {};
          if (annotation_history[resumeId] && annotation_history[resumeId] > 0) {
            $("#next").prop('disabled', false);
          } else {
            $("#next").prop('disabled', true);
          }
          if (approverName) {
            $("#verify").prop('disabled', false);
            $("#next").prop('disabled', false);
          } else {
            $("#verify").prop('disabled', true);
          }
          return self._apiRequest('read', data, self._onLoadAnnotations);
        }
      });

    };

    Store.prototype._onLoadAnnotations = function (data) {
      data = data.rows;
      annotation_history = localStorage.getItem('history') || {};
      var resumeId = localStorage.getItem('currentResumeId');
      if ((annotation_history[resumeId] && annotation_history[resumeId] > 0) || data.length > 0) {
        $("#next").prop('disabled', false);
        annotation_history[resumeId] = data.length;
        localStorage.setItem('history', annotation_history)
      } else {
        $("#next").prop('disabled', true);
      }
      var a, annotation, annotationMap, newData, _i, _j, _len, _len1, _ref;
      if (data == null) {
        data = [];
      }
      annotationMap = {};
      _ref = this.annotations;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        a = _ref[_i];
        annotationMap[a.id] = a;
      }
      newData = [];
      for (_j = 0, _len1 = data.length; _j < _len1; _j++) {
        a = data[_j];
        // a = JSON.parse(a);
        if (annotationMap[a.id]) {
          annotation = annotationMap[a.id];
          this.updateAnnotation(annotation, a);
        } else {
          newData.push(a);
        }
      }
      this.annotations = this.annotations.concat(newData);
      return this.annotator.loadAnnotations(newData.slice());
    };

    Store.prototype.loadAnnotationsFromSearch = function (searchOptions) {

      return this._apiRequest('search', searchOptions, this._onLoadAnnotationsFromSearch);
    };

    Store.prototype._onLoadAnnotationsFromSearch = function (data) {
      if (data == null) {
        data = {};
      }
      return this._onLoadAnnotations(data.rows || []);
    };

    Store.prototype.dumpAnnotations = function () {
      var ann, _i, _len, _ref, _results;
      _ref = this.annotations;
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        ann = _ref[_i];
        _results.push(JSON.parse(this._dataFor(ann)));
      }
      return _results;
    };

    Store.prototype._apiRequest = function (action, obj, onSuccess) {
      var id, resumeId, options, request, url;
      id = obj && obj.id;
      resumeId = obj && obj.resumeId;
      url = 'http://192.168.3.12' + this._urlFor(action, id, resumeId);
      if (action === 'destroy') {
        // A brute force
        url = url.replace('test', resumeId);
      }
      options = action === 'read' ? this._apiRequestOptions(action, null, onSuccess) : this._apiRequestOptions(action, obj, onSuccess);
      request = $.ajax(url, options);
      request._id = id;
      request._action = action;
      return request;
    };

    Store.prototype._apiRequestOptions = function (action, obj, onSuccess) {
      var data, method, opts;
      method = this._methodFor(action);
      headers = this.element.data('annotator:headers') || {};
      headers['username'] = localStorage.getItem('userName');
      opts = {
        type: method,
        headers: headers,
        dataType: "json",
        success: onSuccess || function () { },
        error: this._onError
      };
      if (this.options.emulateHTTP && (method === 'PUT' || method === 'DELETE')) {
        opts.headers = $.extend(opts.headers, {
          'X-HTTP-Method-Override': method
        });
        opts.type = 'POST';
      }
      if (action === "search") {
        opts = $.extend(opts, {
          data: obj
        });
        return opts;
      }
      data = obj && this._dataFor(obj);
      if (this.options.emulateJSON) {
        opts.data = {
          json: data
        };
        if (this.options.emulateHTTP) {
          opts.data._method = method;
        }
        return opts;
      }
      opts = $.extend(opts, {
        data: data,
        contentType: "application/json; charset=utf-8"
      });
      return opts;
    };

    Store.prototype._urlFor = function (action, id, resumeId) {
      var url;
      url = this.options.prefix != null ? this.options.prefix : '';
      url += this.options.urls[action];
      url = url.replace(/\/:id/, id != null ? '/' + id : '');
      url = url.replace(/:id/, id != null ? id : '');
      url = url.replace(/\/:resumeId/, resumeId != null ? '/' + resumeId : '');
      url = url.replace(/:resumeId/, resumeId != null ? resumeId : '');
      return url;
    };

    Store.prototype._methodFor = function (action) {
      var table;
      table = {
        'create': 'POST',
        'read': 'GET',
        'update': 'PUT',
        'destroy': 'DELETE',
        'search': 'GET'
      };
      return table[action];
    };

    Store.prototype._dataFor = function (annotation) {
      var data, highlights;
      highlights = annotation.highlights;
      delete annotation.highlights;
      $.extend(annotation, this.options.annotationData);
      annotation.resumeId = localStorage.getItem('currentResumeId');
      data = JSON.stringify(annotation);
      if (highlights) {
        annotation.highlights = highlights;
      }
      return data;
    };

    Store.prototype._onError = function (xhr) {
      var action, message;
      action = xhr._action;
      message = Annotator._t("Sorry we could not ") + action + Annotator._t(" this annotation");
      if (xhr._action === 'search') {
        message = Annotator._t("Sorry we could not search the store for annotations");
      } else if (xhr._action === 'read' && !xhr._id) {
        message = Annotator._t("Sorry we could not ") + action + Annotator._t(" the annotations from the store");
      }
      switch (xhr.status) {
        case 401:
          message = Annotator._t("Sorry you are not allowed to ") + action + Annotator._t(" this annotation");
          break;
        case 404:
          message = Annotator._t("Sorry we could not connect to the annotations store");
          break;
        case 500:
          message = Annotator._t("Sorry something went wrong with the annotation store");
      }
      Annotator.showNotification(message, Annotator.Notification.ERROR);
      return console.error(Annotator._t("API request failed:") + (" '" + xhr.status + "'"));
    };

    return Store;

  })(Annotator.Plugin);

}).call(this);
