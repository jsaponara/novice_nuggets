
'''
Welcome to the first novice nugget!  

These are based on real production code at a large and reputable company.
Most likely it was written by someone very smart, but new to python,
without a handy local python expert to turn to.  So they just did what
they were certain would work, even though they likely suspected there
was a better way.  Your task is to find that way.
'''

'''
addendum: what we learned from this first nugget:
    nuggets should be runnable.
'''

###############
# part 1: simplify this function:

def send_mail_1(
    unit_of_work,
    sender, recipients, subject, body,
    path=None, attachments=None,
    cc_recipients=None, bcc_recipients=None
):  
    if path is None:
        _send_mail(
            unit_of_work=unit_of_work,
            sender=sender,
            recipients=recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            subject=subject,
            body=body,
            attachments=attachments,
        )
    else:
        _send_mail(
            unit_of_work=unit_of_work,
            sender=sender,
            recipients=recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            subject=subject,
            body=body,
            attachments=attachments,
            path=path
        )


###############
# part 2: simplify this function:
# try to ignore the odd double use [as both context and argument] of unit_of_work.

def send_mail_2(
    sender, recipients, subject, body,
    path=None, attachments=None,
    cc_recipients=None, bcc_recipients=None,
    unit_of_work=None
):  
    if unit_of_work is not None:
        _send_mail(
            unit_of_work=unit_of_work,
            sender=sender,
            recipients=recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            subject=subject,
            body=body,
            path=path,
            attachments=attachments
        )
    else:
        with new_unit_of_work('send_mail') as unit_of_work:
            _send_mail(
                unit_of_work=unit_of_work,
                sender=sender,
                recipients=recipients,
                cc_recipients=cc_recipients,
                bcc_recipients=bcc_recipients,
                subject=subject,
                body=body,
                path=path,
                attachments=attachments
            )


################
# definitions just to make the code above run:

class UnitOfWork:

    def __init__(self, unit_name, is_auto_commit):
        self.unit_name = unit_name
        self.is_auto_commit = is_auto_commit

    # this class is a context manager
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, tb):
        pass

    def __repr__(self):
        return 'UnitOfWork(%(unit_name)s, %(is_auto_commit)s)' % self.__dict__

def new_unit_of_work(unit_name, is_auto_commit=False):
    return UnitOfWork(unit_name, is_auto_commit)

def _send_mail(
    unit_of_work,
    sender, recipients, subject, body,
    attachments=None,
    cc_recipients=None, bcc_recipients=None,
    path=None
):  
    pass


################
# call the functions

unit_of_work = None
sender = 'sender'
recipients = ['recipient1', 'recipient2']
subject = 'subject'
body = 'body'
path = '/a/b/filename.txt'

send_mail_1(
    unit_of_work,
    sender, recipients, subject, body,
    path
)  
send_mail_2(
    sender, recipients, subject, body,
    unit_of_work
)  

