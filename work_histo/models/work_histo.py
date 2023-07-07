# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WorkHistoLine(models.Model):
    _name = 'work.histo.line'
    _description = "work history line"

    work_histo_id = fields.Many2one('work.histo', string='Wizard')
    name = fields.Char(string='Name')
    actions = fields.Selection([('keep', 'Laisser Les Taches Actives (Pas de changement de statut)'),
                                ('permis',
                                 'Terminer Les Taches(Retire les taches du tableau de bord mais reste affichable après recherche)'),
                                ('archiv',
                                 'Archiver Les Taches Sélectionnées(Retire les taches du tableau de bord et de la recherche)'),
                                ('suspend', 'Suspendre Temporairement Les Taches Encours'),
                                ('treated', 'Cloturer Définitivement Les Taches Encours'),
                                ('cancel', 'Annuler Les Taches Encours'),
                                ], readonly=True, string='Action WF')
    type = fields.Selection([
        ('affect_inter', 'Affectation Intervenant'),
        ('affect_control', 'Affectation Controle'),
        ('affect_corr', 'Affectation Correction'),
        ('duplication', 'Duplication'),
        ('aw', 'Action Workflow'),
        ('db', 'Déclaration des Bons'),
        ('db_con', 'Déclaration Bon Controle'),
        ('db_corr', 'Déclaration Bon correction'),
        ('cp', 'Cloture Projet'),
        ('subdivision', 'Subdivision')],
        string='Type', readonly=True)
    date = fields.Date(string='Date Création')
    create_by = fields.Char(string='Crée par')
    execute_by = fields.Char(string='Exécuté par')
    id_object = fields.Integer(string='ID Objet')
    lien_ftp = fields.Char(string='Lien FTP')
    coment1 = fields.Char(string='Commentaire1')
    coment2 = fields.Char(string='Commentaire2')
    coment3 = fields.Char(string='Commentaire3')
    coment4 = fields.Char(string='Commentaire4')

    def action_open_object(self):
        current = self[0]
        if current.type == 'affect_inter':
            return {
                'name': ('Affectation Intervenant'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                # 'views':[[1677,'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.invoices.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'affect_control':
            return {
                'name': ('Affectation Controle'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                # 'views':[[1677,'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.invoices.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'affect_corr':
            return {
                'name': ('Affectation Correction'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                # 'views':[[1677,'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.invoices.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'duplication':
            return {
                'name': ('Duplication'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[1473, 'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.work.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'aw':
            return {
                'name': ('Action Workflow'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[1699, 'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.flow.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'db':
            return {
                'name': ('Déclaration des Bons'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[1543, 'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.group.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'db_con':
            return {
                'name': ('Déclaration Bon Controle'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[1664, 'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.group.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'db_corr':
            return {
                'name': ('Déclaration Bon Correction'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[1665, 'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'base.group.merge.automatic.wizard',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        elif current.type == 'cp':
            return {
                'name': ('Cloture Projet'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[325, 'form']],
                'target': 'popup',
                'auto_search': False,
                'res_model': 'project.project',
                'res_id': current.id_object,
                'context': {},
                'domain': []
            }
        else:
            return True


class WorkHisto(models.Model):
    _name = "work.histo"
    _description = "work history"

    name = fields.Char(string='Nom')
    work_histo_line_id = fields.One2many('work.histo.line', 'work_histo_id', string=u"Histo lines", copy=True)
    date = fields.Date(string='Date Ajout Task')
    create_by = fields.Char(string='Crée par')
    create_a = fields.Date(string='Crée le')
    zone = fields.Char(string='zone')
    secteur = fields.Char(string='secteur')
    project_id = fields.Many2one('project.project', string='Projet')
    task_id = fields.Many2one('project.task', string='Task')
    categ_id = fields.Many2one('product.category', string='Département')
    work_id = fields.Many2one('project.task.work', string='Tache')
    product_id = fields.Many2one('product.product', string='Type de service')
    partner_id = fields.Many2one('res.partner', string='Client')
    work_sup_id = fields.Many2one('work.histo', string='Tache Source de Subdivision')

    def action_open_work_sup(self):
        current = self[0]
        if current.work_sup_id:
            return {
                'name': 'Historique',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'popup',
                'res_model': 'work.histo',
                'res_id': current.work_sup_id.id,
                'context': {},
                'domain': []
            }
        else:
            raise UserError(_("Error !\nVous n'avez aucune subdivision sur cette tache!!!"))
