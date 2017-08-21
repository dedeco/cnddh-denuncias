# -*- coding: utf-8 -*-

from wtforms import Form
from wtforms import validators
from wtforms import SelectMultipleField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.fields import IntegerField, BooleanField
from cnddh.database import db
from cnddh.models import Cidade, Status, TipoLocal, TipoViolacao
from cnddh.models import TipoVitima, TipoSuspeito, TipoFonte, TipoMeioUtilizado

from cnddh.mapeamentos import (estados_choices, sexo_choices, cor_choices,
                               periodo_choices)


class ExportToExcelFiltroForm(Form):
    """Form to specific filter to create sheet."""

    class Meta:
        """Just set language to form. For mesage erros."""

        locales = ['pt_BR', 'pt']

    def __init__(self, *args, **kwargs):
        """O formulário precisa de opções para o select."""
        """Essas opções são iniciadas nesse init."""
        super(ExportToExcelFiltroForm, self).__init__(*args, **kwargs)

        status = db.session.query(Status).order_by(Status.status).distinct()

        cidades = db.session.query(Cidade.cidade).order_by(
            Cidade.cidade).distinct()
        self.cidades.choices = map(lambda item: (item.cidade, item.cidade),
                                   cidades)

        self.status_denuncia.choices = map(
            lambda item: (str(item.id), item.status), status)

        tipo_de_locais = db.session.query(TipoLocal).order_by(
            TipoLocal.local).distinct()
        self.tipo_de_locais.choices = map(
            lambda item: (str(item.id), item.local), tipo_de_locais)

        violacoes_macrocategoria = db.session.query(
            TipoViolacao.macrocategoria).order_by(
                TipoViolacao.macrocategoria).distinct(
                    TipoViolacao.macrocategoria)
        violacoes_microcategoria = db.session.query(
            TipoViolacao.microcategoria).order_by(
                TipoViolacao.microcategoria).distinct(
                    TipoViolacao.microcategoria)
        self.violacoes_macrocategoria.choices = map(
            lambda item: (item.macrocategoria, item.macrocategoria),
            violacoes_macrocategoria)
        self.violacoes_microcategoria.choices = map(
            lambda item: (item.microcategoria, item.microcategoria),
            violacoes_microcategoria)

        tipo_de_vitimas = db.session.query(TipoVitima).order_by(
            TipoVitima.tipo).distinct()
        self.tipo_de_vitimas.choices = tipo_de_vitimas = map(
            lambda item: (str(item.id), item.tipo), tipo_de_vitimas)

        tipo_suspeito_tipo = db.session.query(TipoSuspeito.tipo).order_by(
            TipoSuspeito.tipo).distinct()
        tipo_suspeito_instituicao = db.session.query(
            TipoSuspeito.instituicao).order_by(
                TipoSuspeito.instituicao).distinct()
        # TOdo One Query for both
        self.tipo_de_suspeitos_tipo.choices = map(
            lambda item: (item.tipo, item.tipo), tipo_suspeito_tipo)
        self.tipo_de_suspeitos_instituicao.choices = map(
            lambda item: (item.instituicao, item.instituicao),
            tipo_suspeito_instituicao)

        tipo_de_fontes = db.session.query(TipoFonte).order_by(
            TipoFonte.tipofonte)
        self.tipo_de_fontes.choices = map(
            lambda item: (str(item.id), item.tipofonte), tipo_de_fontes)

        tipo_de_meio = db.session.query(TipoMeioUtilizado).order_by(
            TipoMeioUtilizado.meio)
        self.meio_utilizado.choices = map(
            lambda item: (str(item.id), item.meio), tipo_de_meio)

    cidades = SelectMultipleField(u"Cidades", [], choices=[])
    estados = SelectMultipleField(u"Estados", [], choices=estados_choices)
    status_denuncia = SelectMultipleField(u"Status Denúncia", [], choices=[])
    tipo_de_locais = SelectMultipleField(u"Tipo de locais", [], choices=[])
    tipo_de_fontes = SelectMultipleField(u"Tipo de fontes", [], choices=[])

    violacoes_macrocategoria = SelectMultipleField(
        u"Violações Macro Categoria", [], choices=[])
    violacoes_microcategoria = SelectMultipleField(
        u"Violações Macro Categoria", [], choices=[])
    tipo_de_vitimas = SelectMultipleField(u"Tipo de Vítimas", [], choices=[])
    quantidade_de_vitimas_inicio = IntegerField(u"Quantidade de vítimas", [
        validators.optional(),
        validators.NumberRange(0, 50)
    ])
    quantidade_de_vitimas_fim = IntegerField(u"Quantidade de vítimas", [
        validators.optional(),
        validators.NumberRange(0, 50)
    ])
    data_criacao_inicio = DateField(u'Data criação inicio',
                                    [validators.optional()])
    data_criacao_fim = DateField(u'Data criação fim', [validators.optional()])
    data_denuncia_inicio = DateField(u'Data denúncia', [validators.optional()])
    data_denuncia_fim = DateField(u'Data denúncia', [validators.optional()])
    sexo_vitima = SelectMultipleField(u"Sexo", [], choices=sexo_choices)
    cor_vitima = SelectMultipleField(u"Cor", [], choices=cor_choices)

    vitima_idade_inicio = IntegerField(u"Idade", [validators.optional()])
    vitima_idade_fim = IntegerField(u"Idade", [validators.optional()])

    tipo_de_suspeitos_tipo = SelectMultipleField(
        u"Tipo de Suspeitos", [], choices=[])
    tipo_de_suspeitos_instituicao = SelectMultipleField(
        u"Tipo de Suspeitos", [], choices=[])
    quantidade_de_suspeitos_inicio = IntegerField(u"Quantidade de suspeitos", [
        validators.optional(),
        validators.NumberRange(0, 50)
    ])
    quantidade_de_suspeitos_fim = IntegerField(u"Quantidade de suspeitos", [
        validators.optional(),
        validators.NumberRange(0, 50)
    ])
    sexo_suspeito = SelectMultipleField(u"Sexo", [], choices=sexo_choices)
    cor_suspeito = SelectMultipleField(u"Cor", [], choices=cor_choices)

    suspeito_idade_inicio = IntegerField(u"Idade", [validators.optional()])
    suspeito_idade_fim = IntegerField(u"Idade", [validators.optional()])

    homicidio_periodo = SelectMultipleField(
        u"Homicídio período", [], choices=periodo_choices)
    meio_utilizado = SelectMultipleField(u"Meio utilizado", [], choices=[])

    recuperar_encaminhamentos = BooleanField(u"Recuperar Encaminhamentos", [])
    data_formato = SelectField(
        u'Data Formato', choices=[('dd/mm/yyyy', 'Normal'), ('yyyy', 'Ano')])
    # TODO FIltro encaminhamento e retorno?
