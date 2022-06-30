function send_email(subject,message,varargin)
%% Using dummy hotmail account
email   = 'afishertest@hotmail.com';
password    = 'Password123!@#';

%% Set SMTP properties, enable authentication
setpref('Internet','E_mail',email);
setpref('Internet','SMTP_Server','smtp-mail.outlook.com');
setpref('Internet','SMTP_Username',email);
setpref('Internet','SMTP_Password',password);
props   = java.lang.System.getProperties;
props.setProperty('mail.smtp.auth','true');
props.setProperty('mail.smtp.starttls.enable','true');

%% Send Message
if nargin==2
    sendmail(email,subject,message);
elseif nargin==3
    sendmail(email,subject,message,varargin{1});
else
    errormsg('Incorrect number of inputs');
end

fprintf('Email Sent\n');
end