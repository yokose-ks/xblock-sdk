"""TO-DO: Write a description of what this XBlock is."""

import json
import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Boolean, Dict, Integer, List, String
from xblock.fragment import Fragment
from django.template import Context, Template


class PollXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    display_name = String(display_name="Display Name",
                          default="Poll XBlock",
                          scope=Scope.settings,
                          help="Name of the component in the edX platform")

    voted = Boolean(help="Whether this student has voted on the poll", scope=Scope.user_state, default=False)
    poll_answer = String(help="Student answer", scope=Scope.user_state, default="")
    poll_answers = Dict(help="All possible answers for the poll fro other students", scope=Scope.user_state_summary)

    # List of answers, in the form {'id': 'some id', 'text': 'the answer text'}
    answers = List(help="Poll answers from xml", scope=Scope.content, default=[])

    question = String(help="Poll question", scope=Scope.content, default="")

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the PollXBlock, shown to students
        when viewing courses.
        """
        template = Template(self.resource_string("static/html/pollxblock.html"))
        html = template.render(Context({
            'configuration_json': json.dumps({
                "answers": {"yes": "Yes", "no": "No", "other": "Can\'t say"},
                "question": "<p>Do you agree with having the right to collective self-defense under international law?</p>",
                "poll_answer": self.poll_answer,
                "poll_answers": self.poll_answers if self.voted else {},
                "total": sum(self.poll_answers.values()),
                # TODO: str(self.descriptor.xml_attributes.get('reset', 'true')).lower()
                "reset": "true"
            })
        }))
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/pollxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/pollxblock.js"))
        frag.initialize_js('PollXBlock')
        return frag

#    def dump_poll(self):
#        """Dump poll information.
#
#        Returns:
#            string - Serialize json.
#        """
#        # FIXME: hack for resolving caching `default={}` during definition
#        # poll_answers field
#        if self.poll_answers is None:
#            self.poll_answers = {}
#
#        answers_to_json = OrderedDict()
#
#        # FIXME: fix this, when xblock support mutable types.
#        # Now we use this hack.
#        temp_poll_answers = self.poll_answers
#
#         # Fill self.poll_answers, prepare data for template context.
#        for answer in self.answers:
#            # Set default count for answer = 0.
#            if answer['id'] not in temp_poll_answers:
#                temp_poll_answers[answer['id']] = 0
#            answers_to_json[answer['id']] = cgi.escape(answer['text'])
#        self.poll_answers = temp_poll_answers
#
#        return json.dumps({'answers': answers_to_json,
#            'question': cgi.escape(self.question),
#            # to show answered poll after reload:
#            'poll_answer': self.poll_answer,
#            'poll_answers': self.poll_answers if self.voted else {},
#            'total': sum(self.poll_answers.values()) if self.voted else 0,
#            'reset': str(self.descriptor.xml_attributes.get('reset', 'true')).lower()})

    @XBlock.json_handler
    def get_state(self, data, suffix=''):
        """
        """
        #return {"total": 0,
        #        "poll_answer": "yes",
        #        "poll_answers": {"yes": 1, "other": 0, "no": 0}}
        return {'poll_answer': self.poll_answer,
                'poll_answers': self.poll_answers,
                'total': sum(self.poll_answers.values())}

    @XBlock.json_handler
    def answer_poll(self, data, suffix=''):
        """
        """
        poll_answer = data['poll_answer']
        self.poll_answers[poll_answer] += 1

        self.voted = True
        self.poll_answer = poll_answer

        return {"total": 1,
                "poll_answers": {"yes": 1, "other": 0, "no": 0},
                "callback": {"objectName": "Conditional"}}

    @XBlock.json_handler
    def reset_poll(self, data, suffix=''):
        """
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        #return {"status": "success"}
        return {
            'status': 'success',
        }

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PollXBlock",
             """<vertical_demo>
                <pollxblock/>
                </vertical_demo>
             """),
        ]