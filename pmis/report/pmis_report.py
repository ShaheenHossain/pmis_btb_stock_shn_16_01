from odoo import fields, models,_, api
from datetime import date, datetime, time
from odoo.exceptions import  ValidationError


class pmisReports(models.TransientModel):
    _name = "pmis.report.wizard"
    report_type = fields.Selection(string='Report Type',
                                    selection=[('short', 'Short'), ('long', 'Long'),('custom', 'Custom')], default='short')
    officer_ids=fields.Many2many('res.partner',string="Officers")
    family_info=fields.Boolean(string="Family Info")
    # child_info=fields.Boolean(string="Children Info")
    education_info=fields.Boolean(string="Education Info")

    joining_info=fields.Boolean(string="Joining Info")
    job_info=fields.Boolean(string="Job Info")
    promotion_info=fields.Boolean(string="Promotion Info")
    leave_info=fields.Boolean(string="Leave Info")
    pay_fixation_info=fields.Boolean(string="Pay Fixation Info")
    disciplin_info=fields.Boolean(string="Disciplinery Actions")
    disciplin_info=fields.Boolean(string="Disciplinery Actions")
    case_info=fields.Boolean(string="Case Filed")
    language_info=fields.Boolean(string="Language Proficiency")
    training_info=fields.Boolean(string="Training Details")
    senior_scale_info=fields.Boolean(string="Senior Scale Exams")
    travel_info=fields.Boolean(string="Foreign Travel Details")
    award_info=fields.Boolean(string="Award Details")
    publication_info=fields.Boolean(string="Publication Details")
    sports_info=fields.Boolean(string="Sports Details")
    research_info=fields.Boolean(string="Research Details")
    addl_qualification_info=fields.Boolean(string="Addl Qualification Details")

    @api.onchange("report_type")
    def prepare_report(self):
        if self.report_type=="short":
            self.family_info = True
            self.education_info = True

            self.joining_info = False
            self.job_info = True
            self.promotion_info = False
            self.leave_info =False
            self.pay_fixation_info = False
            self.disciplin_info =False
            self.disciplin_info = False
            self.case_info = False
            self.language_info = False
            self.training_info = False
            self.senior_scale_info = False
            self.travel_info = False
            self.award_info = False
            self.publication_info = False
            self.sports_info = False
            self.research_info = False
            self.addl_qualification_info = False

        elif self.report_type=="long":
            self.family_info = True
            self.education_info = True

            self.joining_info = True
            self.job_info = True
            self.promotion_info = False
            self.leave_info =False
            self.pay_fixation_info = False
            self.disciplin_info =True
            self.disciplin_info = False
            self.case_info = False
            self.language_info = True
            self.training_info = False
            self.senior_scale_info = False
            self.travel_info = False
            self.award_info = False
            self.publication_info = False
            self.sports_info = False
            self.research_info = False
            self.addl_qualification_info = False

    def print_report(self):
        for person in self.officer_ids:
            len(person.posting_records.ids)

        #     Todo call report from python
        return self.env.ref('pmis.pmis_print_custom_report').report_action(self.ids)