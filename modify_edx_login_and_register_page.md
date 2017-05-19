> 目标：我们要找到登录时对应的html页面，进行修改。

1. **首先：由于edx登录时所用的url是：http://cherry.cs.tsinghua.edu.cn/login
因此，我们通过查看urls.py文件中login对应的模板，可以知道对应的html路径**

```
sudo vi /edx/app/edxapp/edx-platform/lms/urls.py
```

可以找到下面的代码：
```
if settings.FEATURES["ENABLE_COMBINED_LOGIN_REGISTRATION"]:
 # Backwards compatibility with old URL structure, but serve the new views
 urlpatterns += (
 url(r'^login$', 'student_account.views.login_and_registration_form',
 {'initial_mode': 'login'}, name="signin_user"),
 url(r'^register$', 'student_account.views.login_and_registration_form',
 {'initial_mode': 'register'}, name="register_user"),
 )
```

上面的
```
student_account.views.login_and_registration_form
```
指明了login页面来自student_account目录下，其中的login_and_registration_form部分定义


2. **其次： 找到student_account目录**

/edx/app/edxapp/edx-platform/lms/templates/student_account

在该目录下可以看到```login_and_register.html``` 和```login.underscore```这两个与login有关的文件

login_and_register.html中的这部分内容
```


<%block name="header_extras">
    % for template_name in ["account", "access", "form_field", "login", "register",
 "institution_login", "institution_register", "password_reset", "hinted_login"]:
 <script type="text/template" id="${template_name}-tpl">
            <%static:include path="student_account/${template_name}.underscore" />
        </script>
% endfor
</%block>

```

指明了静态文件的路径：  <%static:include path="student_account/${template_name}.underscore" />

因此我们找到
/edx/app/edxapp/edx-platform/lms/templates/student_account/login.underscore这个文件就是实际定义登录页面的文件了！

form表单里的内容就是页面的定义：
```
<form id="login" class="login-form" tabindex="-1">

 <div class="section-title lines">
 <h2>
 <span class="text"><%- gettext("Sign in") %></span>
 </h2>
    </div>

 <p class="sr">
 <% if ( context.providers.length > 0 && !context.currentProvider || context.hasSecondaryProviders ) { %>
 <%- gettext("Sign in here using your email address and password, or use one of the providers listed below.") %>
 <% } else { %>
 <%- gettext("Sign in here using your email address and password.") %>
 <% } %>
 <%- gettext("If you do not yet have an account, use the button below to register.") %>
    </p>

 <%= context.fields %>

 <button type="submit" class="action action-primary action-update js-login login-button"><%- gettext("Sign in") %></button>

 <% if ( context.providers.length > 0 && !context.currentProvider || context.hasSecondaryProviders ) { %>
    <div class="login-providers">
 <div class="section-title lines">
 <h2>
 <span class="text"><%- gettext("or sign in with") %></span>
 </h2>
 </div>
  <% _.each( context.providers, function( provider ) {
 if ( provider.loginUrl ) { %>
 <button type="button" class="button button-primary button-<%- provider.id %> login-provider login-<%- provider.id %>" data-provider-url="<%- provider.loginUrl %>">
 <div class="icon <% if ( provider.iconClass ) { %>fa <%- provider.iconClass %><% } %>" aria-hidden="true">
 <% if ( provider.iconImage ) { %>
 <img class="icon-image" src="<%- provider.iconImage %>" alt="<%- provider.name %> icon" />
 <% } %>
 </div>
 <span aria-hidden="true"><%- provider.name %></span>
 <span class="sr"><%- _.sprintf( gettext("Sign in with %(providerName)s"), {providerName: provider.name} ) %></span>
 </button>
 <% }
 }); %>

 <% if ( context.hasSecondaryProviders ) { %>
 <button type="button" class="button-secondary-login form-toggle" data-type="institution_login">
 <%- gettext("Use my institution/campus credentials") %>
 </button>
 <% } %>
 </div>
 <% } %>
</form>
```

把不需要的内容删除，form表单内容如下：
```
<form id="login" class="login-form" tabindex="-1">
 <% if ( context.providers.length > 0 && !context.currentProvider || context.hasSecondaryProviders ) { %>
    <div class="login-providers">
 <div class="section-title lines">
 <h2>
 <span class="text"><%- gettext(" sign in with") %></span>
 </h2>
 </div>

 <% _.each( context.providers, function( provider ) {
 if ( provider.loginUrl ) { %>
 <button type="button" class="button button-primary button-<%- provider.id %> login-provider login-<%- provider.id %>" data-provider-url="<%- provider.loginUrl %>">
 <div class="icon <% if ( provider.iconClass ) { %>fa <%- provider.iconClass %><% } %>" aria-hidden="true">
 <% if ( provider.iconImage ) { %>
 <img class="icon-image" src="<%- provider.iconImage %>" alt="<%- provider.name %> icon" />
 <% } %>
 </div>
 <span aria-hidden="true"><%- provider.name %></span>
 <span class="sr"><%- _.sprintf( gettext("Sign in with %(providerName)s"), {providerName: provider.name} ) %></span>
 </button>
 <% }
 }); %>

 <% if ( context.hasSecondaryProviders ) { %>
 <button type="button" class="button-secondary-login form-toggle" data-type="institution_login">
 <%- gettext("Use my institution/campus credentials") %>
 </button>
 <% } %>
 </div>
 <% } %>
</form>
```

保存！登录页面己修改成功！


