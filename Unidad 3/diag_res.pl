% --- Declaración de hechos dinámicos ---
% Usaremos un predicado general sintoma(NombreSintoma, ValorSintoma).
:- dynamic sintoma/2.

% --- Reglas de Diagnóstico ---
% R1 (Resfriado Común)
diagnostico('Resfriado Común') :-
    sintoma(congestion_nasal, si),
    sintoma(estornudos, si),
    sintoma(dolor_garganta, si),
    (sintoma(fiebre, ausente); sintoma(fiebre, baja)),
    \+ sintoma(dolores_musculares, si), % Ausencia de dolores musculares generales
    \+ sintoma(fatiga, si).             % Ausencia de fatiga general

% R2 (Gripe/Influenza)
diagnostico('Gripe/Influenza') :-
    sintoma(fiebre, alta),
    sintoma(dolores_musculares, intensos),
    sintoma(fatiga, intensa),
    sintoma(tos, seca),
    (sintoma(dolor_cabeza, si); sintoma(dolor_garganta, si)),
    sintoma(duracion_sintomas, '< 10 dias').

% R3 (Alergia Respiratoria)
diagnostico('Alergia Respiratoria') :-
    sintoma(estornudos, frecuentes),
    sintoma(secrecion_nasal, si),
    sintoma(tipo_secrecion, acuosa),
    sintoma(picazon_ojos_nariz, si),
    sintoma(fiebre, ausente),
    (sintoma(historial_alergias, si); sintoma(epoca_año, primavera); sintoma(epoca_año, otoño)).

% R4 (Bronquitis Aguda)
diagnostico('Bronquitis Aguda') :-
    sintoma(tos, productiva),
    (sintoma(tipo_flema, clara); sintoma(tipo_flema, amarilla); sintoma(tipo_flema, verdosa)),
    sintoma(duracion_sintomas, '> 5 dias'),
    sintoma(duracion_sintomas, '< 3 semanas'), % Ambas condiciones de duración deben ser seleccionables
    (sintoma(fiebre, ausente); sintoma(fiebre, baja)),
    (sintoma(dolor_pecho, si); sintoma(fatiga, si)). % Fatiga general

% R5 (Neumonía)
diagnostico('Neumonía') :-
    sintoma(fiebre, alta),
    sintoma(tos, productiva),
    (sintoma(tipo_flema, amarilla); sintoma(tipo_flema, verdosa); sintoma(tipo_flema, herrumbrosa)),
    sintoma(dificultad_respirar, si),
    sintoma(dolor_pecho, si),
    sintoma(fatiga, intensa).

% R6 (Exacerbación Asma)
diagnostico('Exacerbación Asma') :-
    sintoma(dificultad_respirar, si),
    sintoma(sibilancias, si),
    (sintoma(tos, seca); sintoma(tos, productiva)),
    sintoma(historial_asma, si).

% R7 (COVID-19)
diagnostico('COVID-19') :-
    (sintoma(fiebre, alta); sintoma(fiebre, baja)), % Podría ser ausente también según variantes. Simplificado aquí.
    (sintoma(tos, seca); sintoma(tos, productiva)),
    (sintoma(fatiga, intensa); sintoma(dificultad_respirar, si); sintoma(perdida_olfato_gusto, si); sintoma(dolores_musculares, si)), % Dolores musculares generales
    (sintoma(contacto_enfermo, si); sintoma(contacto_enfermo, desconocido)).

% R8 (Posible Coccidioidomicosis)
diagnostico('Posible Coccidioidomicosis') :-
    (sintoma(fiebre, baja); sintoma(fiebre, alta)),
    sintoma(tos, seca),
    sintoma(fatiga, si), % Fatiga general
    sintoma(dolor_cabeza, si),
    (sintoma(dolor_pecho, si); sintoma(dolores_musculares, si)), % Dolores musculares generales
    sintoma(duracion_sintomas, 'semanas/meses'),
    sintoma(exposicion_polvo_tierra, si).

% --- Predicado para encontrar todos los diagnósticos posibles ---
encontrar_diagnosticos(ListaDiagnosticos) :-
    findall(Diagnostico, diagnostico(Diagnostico), DiagnosticosDuplicados),
    sort(DiagnosticosDuplicados, ListaDiagnosticos). % sort elimina duplicados

% --- Limpiar hechos para nueva consulta ---
limpiar_sintomas :-
    retractall(sintoma(_, _)).