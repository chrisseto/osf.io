<%inherit file="project/project_base.mako"/>

## Use full page width
<%def name="container_class()">container-xxl</%def>

<%def name="title()">${file_name | h}</%def>

    <div>
        <h2 class="break-word">
            ${file_name | h}
            % if file_revision:
                <small>&nbsp;${file_revision | h}</small>
            % endif
        </h2>
        <hr />
    </div>

    <div id="file-container" class="row">

    <div id="file-navigation" class="panel-toggle col-md-3">
        <div class="osf-panel osf-panel-flex hidden-xs">
            <div class="osf-panel-header osf-panel-header-flex" style="display:none">
                <div id="files-search"></div>
                <div id="toggle-icon" class="pull-right">
                    <div class="panel-collapse"> <i class="fa fa-angle-left"> </i> </div>
                </div>
            </div>

            <div class="osf-panel-body osf-panel-body-flex file-page">
                <div id="grid">
                    <div class="fangorn-loading"> <i class="fa fa-spinner fangorn-spin"></i> <p class="m-t-sm fg-load-message"> Loading files...  </p> </div>
                </div>
            </div>
        </div>

    <!-- Menu toggle closed -->
            <div class="osf-panel panel-collapsed hidden-xs text-center"  style="display: none">
              <div class="osf-panel-header">
                <i class="fa fa-file"> </i>
                <i class="fa fa-angle-right"> </i>
              </div>
            </div>

    </div>

    <div class="panel-expand col-md-6">

        <div id="fileRendered" class="mfr mfr-file">
          % if rendered is not None:
            ${rendered}
          % else:
            <img src="/static/img/loading.gif">
          % endif
        </div>
    </div>

      <div class="col-md-3">
        <div id="fileRevisions" class="scripted">
          <ol class="breadcrumb">
            <li><a href="{{ node.urls.files }}" data-bind="text: node.title"></a></li>
            <li class="active overflow" data-bind="text: file.provider"></li>
            <!-- ko foreach: path.slice(1) -->
            <li class="active overflow" data-bind="text: $data"></li>
            <!-- /ko -->
          </ol>

          <span data-bind="if: currentVersion">
            <a class="btn btn-success btn-md file-download" href="{{ currentVersion().osfDownloadUrl }}" data-bind="click: currentVersion().download">
              Download <i class="fa fa-download"></i>
            </a>
          </span>

          <span data-bind="if: editable">
            <button class="btn btn-danger btn-md file-delete" data-bind="click: askDelete">
              Delete <i class="fa fa-trash-o"></i>
            </button>
          </span>


          <table class="table" data-bind="if: versioningSupported && revisions().length">
            <thead>
              <tr>
                <th>Version ID</th>
                <th>Date</th>
                <th data-bind="if: userColumn">User</th>
                <th colspan="2">Download</th>
              </tr>
            </thead>

            <tbody data-bind="foreach: {data: revisions, as: 'revision'}">
              <tr data-bind="css: $parent.isActive(revision)">
                <td>
                  <a href="{{ revision.osfViewUrl }}" data-bind="if: revision !== $parent.currentVersion()">
                    {{ revision.displayVersion }}
                  </a>
                  <span data-bind="if: revision === $parent.currentVersion()">
                    {{ revision.displayVersion }}
                  </span>
                </td>
                <td>{{ revision.displayDate }}</td>
                <td data-bind="if: $parent.userColumn">
                  <a data-bind="if: revision.extra.user.url"
                    href="{{ revision.extra.user.url }}">
                    {{ revision.extra.user.name }}
                  </a>
                  <span data-bind="ifnot: revision.extra.user.url">
                    {{ revision.extra.user.name }}
                  </span>
                </td>
                <td>
                  <span class="badge" data-bind="if: revision.extra.downloads !== undefined">
                    {{ revision.extra.downloads }}
                  </span>
                </td>
                <td>
                  <a class="btn btn-primary btn-sm file-download" href="{{ revision.osfDownloadUrl }}"
                    data-bind="click: revision.download">
                    <i class="fa fa-download"></i>
                  </a>
                </td>
              </tr>
            </tbody>
          </table>

          <div data-bind="ifnot: versioningSupported">
            <hr>
            <div class="alert alert-warning" role="alert">
              {{ errorMessage }}
            </div>
          </div>

        </div>
      </div>
    </div>

  </div>

<%def name="javascript_bottom()">
    ${parent.javascript_bottom()}
    % for script in tree_js:
        <script type="text/javascript" src="${script | webpack_asset}"></script>
    % endfor

    % if 'osf.io' in domain:
    <script>
        // IE10 Same Origin (CORS) fix
        document.domain = 'osf.io';
    </script>
    %endif
    <script type="text/javascript">
      window.contextVars = $.extend(true, {}, window.contextVars, {
    %if rendered is None:
        renderURL: '${render_url | js_str}',
    %else:
        renderURL: undefined,
    %endif
        file: {
            extra: ${extra},
            name: '${file_name | js_str}',
            path: '${file_path | js_str}',
            provider: '${provider | js_str}',
            safeName: '${file_name | h,js_str}'
        },
        node: {
          urls: {
            files: '${files_url | js_str}'
          }
        },
        currentUser: {
          canEdit: ${int(user['can_edit'])}
        }
      });
    </script>
    <script src=${"/static/public/js/view-file-page.js" | webpack_asset}></script>
</%def>
