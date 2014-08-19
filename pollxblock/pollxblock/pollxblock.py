"""TO-DO: Write a description of what this XBlock is."""

import cgi
import json
from collections import OrderedDict
import lxml.etree as etree
import pkg_resources

from xblock.core import XBlock
from xblock.fields import Boolean, Dict, Integer, List, Scope, String
from xblock.fragment import Fragment
from django.template import Context, Template
#from xml import update_from_xml, serialize_content_to_xml


class PollXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """
    display_name = String(help="Name of the component in the edX platform", scope=Scope.settings, default="Poll XBlock")

    voted = Boolean(help="Whether this student has voted on the poll", scope=Scope.user_state, default=False)
    poll_answer = String(help="Student answer", scope=Scope.user_state, default="")
    poll_answers = Dict(help="All possible answers for the poll fro other students", scope=Scope.user_state_summary)

    question = String(help="Poll question", scope=Scope.content, default="Did you enjoy this video?")
    # List of answers, in the form {'id': 'some id', 'text': 'the answer text'}
    answers = List(help="Poll answers", scope=Scope.content, default=[{'id': 'yes', 'text': 'Yes'}, {'id': 'no', 'text': 'No'}, {'id': 'other', 'text': 'No opinion'}])
    reset = Boolean(help="Can reset/revote many time", scope=Scope.content, default=True)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the PollXBlock, shown to students
        when viewing courses.
        """
        template = Template(self.resource_string("static/html/pollxblock.html"))
        html = template.render(Context({
            'configuration_json': self.dump_poll()
        }))
        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/pollxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/pollxblock.js"))
        frag.initialize_js('PollXBlock')
        return frag

    def dump_poll(self):
        """Dump poll information.

        Returns:
            string - Serialize json.
        """
        # FIXME: hack for resolving caching `default={}` during definition
        # poll_answers field
        if self.poll_answers is None:
            self.poll_answers = {}

        answers_to_json = OrderedDict()

        # FIXME: fix this, when xblock support mutable types.
        # Now we use this hack.
        temp_poll_answers = self.poll_answers

         # Fill self.poll_answers, prepare data for template context.
        for answer in self.answers:
            # Set default count for answer = 0.
            if answer['id'] not in temp_poll_answers:
                # TODO(yokose)
                temp_poll_answers[answer['id']] = 0
            answers_to_json[answer['id']] = cgi.escape(answer['text'])
        self.poll_answers = temp_poll_answers

        return json.dumps({'answers': answers_to_json,
            'question': cgi.escape(self.question),
            # to show answered poll after reload:
            'poll_answer': self.poll_answer,
            'poll_answers': self.poll_answers if self.voted else {},
            'total': sum(self.poll_answers.values()) if self.voted else 0,
            'reset': str(self.reset).lower()})

    @XBlock.json_handler
    def get_state(self, data, suffix=''):
        """
        """
        return {'poll_answer': self.poll_answer,
                'poll_answers': self.poll_answers,
                'total': sum(self.poll_answers.values())}

    @XBlock.json_handler
    def answer_poll(self, data, suffix=''):
        """
        """
        if not self.voted:
            poll_answer = data['poll_answer']

            # FIXME: fix this, when xblock will support mutable types.
            # Now we use this hack.
            temp_poll_answers = self.poll_answers
            temp_poll_answers[poll_answer] += 1
            self.poll_answers = temp_poll_answers

            self.voted = True
            self.poll_answer = poll_answer
            return {'poll_answers': self.poll_answers,
                    'total': sum(self.poll_answers.values()),
                    'callback': {'objectName': 'Conditional'}}
        # TODO
        else:  # return error message
            return {'error': 'Unknown Command!'}

    @XBlock.json_handler
    def reset_poll(self, data, suffix=''):
        """
        """
        if self.voted and self.reset:
            self.voted = False

            # FIXME: fix this, when xblock will support mutable types.
            # Now we use this hack.
            temp_poll_answers = self.poll_answers
            temp_poll_answers[self.poll_answer] -= 1
            self.poll_answers = temp_poll_answers

            self.poll_answer = ''
            return {'status': 'success'}
        # TODO
        else:  # return error message
            return {'error': 'Unknown Command!'}

    def studio_view(self, context=None):
        """
        The primary view of the PollXBlock, shown to teachers
        when editing the block.
        """
        template = Template(self.resource_string("static/html/pollxblock_edit.html"))

        #parameters sent to browser for edit html page
        html = template.render(Context({
            'display_name': self.display_name,
            'voted': self.voted,
            'poll_answer': self.poll_answer,
            'poll_answers': self.poll_answers,
            'answers': self.answers,
            'number_of_answers': len(self.answers),
            'question': self.question,
            'reset': self.reset
        }))

        frag = Fragment(html)
        frag.add_css(self.resource_string("static/css/pollxblock_edit.css"))
        frag.add_javascript(self.resource_string("static/js/src/pollxblock_edit.js"))
        frag.initialize_js('PollXBlockEdit')
        return frag

    @XBlock.json_handler
    def save_edit(self, data, suffix=''):
        """
        Handler which saves the json data into XBlock fields.
        """
        self.display_name = data['display_name']
        self.question = data['question']
        self.answers = [{'id': x[0], 'text': x[1]} for x in zip(data['answerIds'], data['answerTexts'])]
        self.reset = data['reset']

        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PollXBlock",
             """<vertical_demo>
                <pollxblock/>
                <pollxblock/>
                </vertical_demo>
             """),
        ]

    @classmethod
    def parse_xml(cls, node, runtime, keys, id_generator):
        """Instantiate XBlock object from runtime XML definition.

        Inherited by XBlock core.

        """
        block = runtime.construct_xblock_from_class(cls, keys)

        return update_from_xml(block, node, validator=validator(block, strict_post_release=False))

    def add_xml_to_node(self, root):
        """
        Serialize the XBlock to XML for exporting.
        """
        root.tag = 'pollxblock'

        if self.display_name is not None:
            root.set('display_name', unicode(self.display_name))

        if self.reset:
            root.set('reset', unicode(self.reset))

        # question
        el_question = etree.SubElement(root, 'question')
        el_question.text = unicode(self.question)

        # answer list
        el_answers = etree.SubElement(root, 'answers')
        for answer in self.answers:
            el_answer = etree.SubElement(el_answers, 'answer')
            el_answer.set('id', unicode(answer['id']))
            el_answer.text = unicode(answer['text'])
