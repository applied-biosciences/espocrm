<div class="container content nuri-login-page">
    <div class="nuri-login-layout">
        <aside class="nuri-brand-story" aria-label="NuriVoyage identity">
            <div class="nuri-company-logo"><img src="client/custom/branding/utnt-logo.png" alt="Umra Tours and Nuri's Travels"></div>
            <p class="nuri-eyebrow">NURI'S TRAVEL</p>
            <h1>NuriVoyage<span class="nuri-gold-dot">.</span></h1>
            <p class="nuri-descriptor">Travel Management Platform</p>
            <p class="nuri-version">v10.0.10.0.s7</p>
            <div class="nuri-brand-rule" aria-hidden="true"></div>
            <p class="nuri-brand-caption">Your journeys.<br>One workspace.</p>
        </aside>
    <div class="container-centering">
        <div id="login" class="panel panel-default block-center-sm">
            <div class="panel-heading nuri-login-heading">
                <p class="nuri-eyebrow">WELCOME BACK</p>
                <h2>Sign in to your workspace</h2>
                <p>Manage your travel, together.</p>
            </div>

            <div class="panel-body{{#if anotherUser}} another-user {{/if}}">
                <div>
                    <form id="login-form">
                        {{#if hasSignIn}}
                            <div class="cell" data-name="sign-in">
                                {{#if hasFallback}}
                                    <div class="pull-right">
                                        <a
                                            role="button"
                                            tabindex="0"
                                            class="btn btn-link btn-icon"
                                            data-action="showFallback"
                                        ><span class="fas fa-chevron-down"></span></a>
                                    </div>
                                {{/if}}
                                <button
                                    class="btn btn-default btn-x-wide"
                                    id="sign-in"
                                    type="button"
                                >{{signInText}}</button>
                            </div>
                        {{/if}}

                        <div class="form-group cell" data-name="username">
                            <label for="field-userName">{{translate 'Username'}}</label>
                            <input
                                type="text"
                                name="username"
                                id="field-userName"
                                class="form-control"
                                autocapitalize="off"
                                spellcheck="false"
                                tabindex="1"
                                autocomplete="username"
                                maxlength="255"
                            >
                        </div>

                        <div class="form-group cell" data-name="password">
                            <label for="field-password">{{translate 'Password'}}</label>
                            <div data-role="password-input-container">
                                <input
                                    type="password"
                                    name="password"
                                    id="field-password"
                                    class="form-control"
                                    tabindex="2"
                                    autocomplete="current-password"
                                    maxlength="255"
                                >
                                <a
                                    role="button"
                                    data-action="toggleShowPassword"
                                    class="text-soft"
                                    title="{{translate 'View'}}"
                                ><span class="far fa-eye"></span></a>
                            </div>
                        </div>

                        {{#if anotherUser}}
                            <div class="form-group cell">
                                <label>{{translate 'Log in as'}}</label>
                                <div>{{anotherUser}}</div>
                            </div>
                        {{/if}}

                        <div class="margin-top-2x cell" data-name="submit">
                            {{#if showForgotPassword ~}}
                                <a
                                    role="button"
                                    class="btn btn-link btn-text btn-text-hoverable btn-sm pull-right margin-top-sm"
                                    data-action="passwordChangeRequest"
                                    tabindex="4"
                                >{{translate 'Forgot Password?' scope='User'}}</a>
                            {{~/if}}
                                <button
                                    type="submit"
                                    class="btn btn-primary btn-s-wide"
                                    id="btn-login"
                                    tabindex="3"
                                >{{logInText}}</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

</div>
<footer>{{{footer}}}</footer>
