def adjustStringCase(stringlist):
    exception_words = {'O': 'o', 'OS': 'os', 'A': 'a', 'DE': 'de', 'EM': 'em', 'POR': 'por', 'AO': 'ao',
                    'DO': 'do', 'NO': 'no', 'PELO': 'pelo', 'AS': 'as', 'AOS': 'aos', 'DOS': 'dos',
                    'NOS': 'nos', 'PELOS': 'pelos', 'UM': 'um', 'À': 'à', 'DA': 'da', 'NA': 'na',
                    'PELA': 'pela', 'UNS': 'uns', 'ÀS': 'às', 'DAS': 'das', 'NAS': 'nas',
                    'PELAS': 'pelas', 'UMA': 'uma', 'DUM': 'dum', 'NUM': 'num', 'UMAS': 'umas',
                    'DUNS': 'duns', 'NUNS': 'nuns', 'DUMA': 'duma', 'NUMA': 'numa',
                    'DUMAS': 'dumas', 'NUMAS': 'numas', 'I': 'I', 'II': 'II', 'II,': 'II,', 
                    'II-': 'II-', 'III': 'III', 'III:': 'III:',
                    'IV': 'IV', 'IV:':'IV:', 'IV:SAUDE': 'IV:Saude', 'V': 'V', 'VI': 'VI', 
                    'VI:': 'VI:', 'VII': 'VII', 'VII:': 'VII:', 'VIII': 'VIII', 'VIII:': 'VIII:', 
                    'IX': 'IX', 'X': 'X', 'XI': 'XI', 'XII': 'XII', 'XIII': 'XIII', 
                    'XIV': 'XIV', 'XV': 'XV', 'XVI': 'XVI', 'XVII': 'XVII', 'XVIII': 'XVIII', 'XVIII-XIX': 'XVIII-XIX', 
                    'XIX': 'XIX', 'XX': 'XX', 'XX-XXI': 'XX-XXI', 'XXI': 'XXI', 'A': 'a', 'AFORA': 'afora',
                    'NA': 'na', 'NAS': 'nas', 'NO': 'no', 'NOS': 'nos', 'DA': 'da',
                    'DAS': 'das', 'DO': 'do', 'DOS': 'dos', 'DAQUILO': 'daquilo', 
                    'NAQUELE': 'naquele', 'NUMA': 'numa', 'DESDE': 'desde', 'MENOS': 'menos',
                    'EM': 'em', 'SALVO': 'salvo', 'ENTRE': 'entre', 'SEGUNDO': 'segundo',
                    'PARA': 'para', 'VISTO': 'visto', 'APÓS': 'após', 'CONFORME': 'conforme', 
                    'ANTE': 'ante', 'COMO': 'como', 'COM': 'com', 'DURANTE': 'durante',
                    'ATÉ': 'até', 'CONSOANTE': 'consoante', 'DE': 'de', 'MEDIANTE': 'mediante',
                    'CONTRA': 'contra', 'EXCETO': 'exceto', 'PER': 'per', 'PERANTE': 'perante',
                    'POR': 'por', 'SEM': 'sem', 'SOB': 'sob', 'SOBRE': 'sobre', 'TRÁS': 'trás',
                    'NEM...': 'nem...', 'E': 'e', 'MAS': 'mas', 'OU': 'ou', 'LOGO': 'logo',
                    'PORQUE': 'porque', 'PORQUANTO': 'porquanto', 'CONTUDO': 'contudo', 'JÁ…': 'já…',
                    'ASSIM': 'assim', 'POIS': 'pois', 'QUER…': 'quer…', 'TODAVIA...': 'todavia...',
                    'ORA…': 'ora…', 'PORTANTO...': 'portanto...', 'ENTRETANTO': 'entretanto', 
                    'ENTÃO': 'então', 'OU…': 'ou…', 'QUE...': 'que...', 'PORÉM': 'porém',
                    'SIM': 'Sim', 'ACASO': 'Acaso', 'ASSAZ': 'Assaz', 'ABAIXO': 'Abaixo',
                    'ASSIM': 'Assim', 'NÃO': 'Não', 'AGORA': 'Agora', 'CERTAMENTE': 'certamente',
                    'PORVENTURA': 'porventura', 'BASTANTE': 'bastante', 'ACIMA': 'acima', 'BEM': 'bem',
                    'TAMPOUCO': 'tampouco', 'AINDA': 'ainda', 'EFETIVAMENTE': 'efetivamente',
                    'POSSIVELMENTE': 'possivelmente', 'ADIANTE': 'adiante', 'DEBALDE': 'debalde', 
                    'ANTES': 'antes', 'AMANHÃ': 'amanhã', 'REALMENTE': 'realmente', 
                    'PROVAVELMENTE': 'provavelmente', 'DEMAIS': 'demais', 
                    'AÍ': 'aí', 'DEPRESSA': 'depressa', 'BREVE': 'breve', 'ANTEONTEM': 'anteontem',
                    'TALVEZ': 'talvez', 'MENOS': 'menos', 'ALI': 'ali', 'MAL': 'mal', 
                    'QUIÇÁ': 'quiçá', 'MAIS': 'mais', 'ALÉM': 'além', 'DEVAGAR': 'devagar',
                    'QUANTO': 'quanto', 'ATRÁS': 'atrás', 'ENTÃO': 'então', 'ONDE': 'onde',
                    'DETRÁS': 'detrás', 'NUNCA': 'nunca', 'QUÃO': 'quão', 'ATRAVÉS': 'através',
                    'HOJE': 'hoje', 'PERTO': 'perto', 'FORA': 'fora', 'ONTEM': 'ontem', 'QUASE': 'quase',
                    'CÁ': 'cá', 'JÁ': 'já', 'MUITO': 'muito', 'AQUÉM': 'aquém', 'MELHOR': 'melhor',
                    'CEDO': 'cedo', 'POUCO': 'pouco', 'AQUI': 'aqui', 'DEPOIS': 'depois',
                    'LÁ': 'lá', 'SEMPRE': 'sempre', 'TÃO': 'tão', 'DENTRO': 'dentro', 'LOGO': 'logo',
                    'LONGE': 'longe', 'JUNTO': 'junto', 'OUTRORA': 'outrora', 'TANTO': 'tanto',
                    'DEFRONTE': 'defronte', 'JAMAIS': 'jamais', '(BIM)': '(BIM)', '(ESG': '(ESG',
                    '(IPI': '(IPI', '(IRPF': '(IRPF', '(ITCD': '(ITCD', '(ITR': '(ITR', '(NC)': '(NC)',
                    '(SCM)': '(SCM)', '.NET': '.NET', 'ANPEC': 'ANPEC', 'AVAC': 'AVAC', 'AVAC-R': 'AVAC-R',
                    'BI': 'BI', 'BIM': 'BIM', 'BPM': 'BPM', 'CEO': 'CEO', 'CFM': 'CFM', 'CORDA': 'CORDA',
                    'CPC': 'CPC', 'CSLL': 'CSLL', 'CSLL:': 'CSLL:', 'CSS': 'CSS', 'DTM': 'DTM', 'EAD': 'EAD',
                    'EE': 'EE', 'EPANET': 'EPANET', 'ESG': 'ESG', 'GDPR': 'GDPR', 'HTML': 'HTML',
                    'ICMS': 'ICMS', 'ICO': 'ICO', 'II:': 'II:', 'IOF': 'IOF', 'IOS': 'IOS', 'IP': 'IP',
                    'IPI': 'IPI', 'IPTU': 'IPTU', 'IPTU)': 'IPTU)', 'IPVA': 'IPVA', 'IRPF': 'IRPF',
                    'IRPJ': 'IRPJ', 'IRPJ)': 'IRPJ)', 'ISO': 'ISO', 'ISS': 'ISS', 'ISS)': 'ISS)',
                    'ITBI': 'ITBI', 'ITBI)': 'ITBI)', 'ITCD': 'ITCD', 'ITR': 'ITR', 'LGPD': 'LGPD', 
                    'MBA': 'MBA', 'MEI': 'MEI', 'NR': 'NR', 'NR09': 'NR09', 'OAB': 'OAB', 'PAR': 'PAR',
                    'PBE': 'PBE', 'PBR': 'PBR', 'PCO': 'PCO', 'PMBOK': 'PMBOK', 'PMG': 'PMG',
                    'PMO': 'PMO', 'PPC': 'PPC', 'PPL': 'PPL', 'PSG': 'PSG', 'PSR': 'PSR', 'PUB': 'PUB',
                    'PUC': 'PUC', 'QSMS': 'QSMS', 'TI': 'TI', 'SGI': 'SGI', 'SIG': 'SIG', 'SQL': 'SQL',
                    'SUS': 'SUS', 'TCP/IP': 'TCP/IP', 'UX': 'UX', '(MODELO)': '(MODELO)', 'ICBS': 'ICBS',
                    'FAPSI': 'FAPSI', 'ICH': 'ICH', 'IPUC': 'IPUC', 'ICEI': 'ICEI', 'ICEG': 'ICEG',
                    'ICS': 'ICS', 'FCA': 'FCA', 'FMD': 'FMD', 'IEC': 'IEC', 'IFTDJ': 'IFTDJ',
                    'NOSQL': 'NoSQL', 'DEVOPS': 'DevOps', 'APIS': 'APIs', 'DAPPS': 'DApps',
                    '(DAPPS)': '(DApps)', 'WEBGIS': 'WebGIS', 'PAAS': 'PaaS', 'DEVSECOPS': 'DevSecOps',
                    'DATAOPS': 'DataOps', 'MLOPS': 'MLOps', 'IOT': 'IoT', 'IOT:': 'IoT:', 'NODE.JS': 'Node.js',
                    'GPSI': 'GPSI', '(GPSI)': '(GPSI)', '(CPPS)': '(CPPS)', 'CPPS': 'CPPS', '(UAN)': '(UAN)', 
                    'UAN': 'UAN', 'SAJ': 'SAJ', '(PPS)': '(PPS)', 'PPS': 'PPS', 'RPG': 'RPG', '(PLM)': '(PLM)',
                    'PLM': 'PLM', 'PI': 'PI', 'TCC': 'TCC', 'TIC': 'TIC', '(TIC)': '(TIC)', 'TEI': 'TEI', 
                    '(TEI)': '(TEI)', 'CD': 'CD', 'CPC/IFRS': 'CPC/IFRS'
                    }
    words = stringlist.upper().split(' ')
    string = ''
    found_exepction = False #Valor é True, quando encontra ':' ou '-'
    first_word = 1
    for word in words:
        if word in exception_words:
            word = exception_words[word]
            if found_exepction or first_word:
                string = string + word.title() + ' ' if word.islower() else string + word + ' '
            else:
                string = string + word + ' '
        else:
            string = string + word.title() + ' '
        first_word = False
        found_exepction = False
        if word and word[-1] == ':': found_exepction = True
        if word == '-': found_exepction = True
    return string.strip()