"""TO-DO: Write a description of what this XBlock is."""

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
            'configuration_json': {
                "reset": "true",
                "poll_answer": "",
                "question": "<p>Do you agree with having the right to collective self-defense under international law?</p>",
                "answers": {"yes": "Yes", "no": "No", "other": "Can\'t say"},
                "poll_answers": {},
                "total": 0
            }
        }))
        frag = Fragment(html)
        #frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/pollxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/pollxblock.js"))
        frag.initialize_js('PollXBlock')
        return frag

    @XBlock.json_handler
    def get_state(self, data, suffix=''):
        """
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"total": 0,
                "poll_answer": "yes",
                "poll_answers": {"yes": 1, "other": 0, "no": 0}}

    @XBlock.json_handler
    def answer_poll(self, data, suffix=''):
        """
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
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
                <pollxblock/>
                <pollxblock/>
                </vertical_demo>
             """),
        ]