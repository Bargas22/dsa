class SuggestStylesService:
    """Catálogo local de sugestões educativas; não analisa fotos nem mede beleza."""
    def execute(self, analysis):
        shape = analysis.face_shape
        hair = analysis.hair_type
        title = 'Topo com volume e laterais suaves' if shape in ('round', 'square') else 'Corte em camadas equilibradas'
        texture = 'Definição de cachos' if hair in ('curly', 'coily') else 'Textura e movimento natural'
        return [
            dict(category='haircut', title=title, description='Converse com o profissional para adaptar o corte.', technical_reason=f'Sugestão do catálogo para formato declarado: {shape}.', compatibility=None),
            dict(category='care', title=texture, description='Ajuste sua rotina de finalização ao tipo de cabelo.', technical_reason=f'Tipo informado: {hair}.', compatibility=None),
            dict(category='beard', title='Contorno natural da barba', description='Ajuste opcional de acabamento com profissional.', technical_reason='Sugestão geral do catálogo.', compatibility=None),
            dict(category='coloring', title='Coloração com avaliação profissional', description='Discuta tonalidade e manutenção antes de mudar.', technical_reason='Sugestão geral; não é uma avaliação de imagem.', compatibility=None),
        ]
