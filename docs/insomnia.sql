type: collection.insomnia.rest/5.0
name: Scratch Pad
meta:
  id: wrk_scratchpad
  created: 1697808478262
  modified: 1697808478262
collection:
  - name: cge_sei
    meta:
      id: fld_b81447ebdbac458fbde681c5419914fb
      created: 1738587841691
      modified: 1738681966180
      sortKey: -1738587841691
  - name: leitura_facil
    meta:
      id: fld_d6b2fe7ab7774edcaf9ed514d1f5cdb4
      created: 1738681938204
      modified: 1738681964695
      sortKey: -1738681938204
  - name: Curso Alura
    meta:
      id: fld_8093b6fb7d3545488c069f7fe97986dd
      created: 1739809304298
      modified: 1740577491139
      sortKey: -1739809304298
  - name: MiguelasNews
    meta:
      id: fld_ab25e17298984abc971087a6e1acc9f8
      created: 1740571256005
      modified: 1741348406475
      sortKey: -1740571256005
  - name: rest_sei
    meta:
      id: fld_12985ad48e5246df8d2a8085c478256f
      created: 1743168289512
      modified: 1743168289512
      sortKey: -1743168289512
  - name: SeiService
    meta:
      id: fld_62934b1c0b224889b896099b6d490314
      created: 1743169396300
      modified: 1743169396300
      sortKey: -1743169387255
    children:
      - name: SeiService
        meta:
          id: fld_c2c12ab9d3d14e6d8228853f81010e4f
          created: 1743169396302
          modified: 1743169396302
          sortKey: -1743169387254
  - name: ecommerce_global
    meta:
      id: fld_62b6e1f43cf141d2a1dd054ff0734734
      created: 1743601054079
      modified: 1744126339200
      sortKey: -1743601054080
    children:
      - name: Usuários
        meta:
          id: fld_ff5961b6b5894286aa8972be117202a3
          created: 0
          modified: 1744023056193
          sortKey: -1743776460048
        children:
          - url: http://127.0.0.1:8000/api/v1/usuarios/
            name: Criar Usuário
            meta:
              id: req_55cd8d81de1240249e4878e8bad555fe
              created: 0
              modified: 1744023075229
              isPrivate: false
              sortKey: -1744022906727
            method: POST
            body:
              mimeType: application/json
              text: |-
                {
                  "nome": "João Silva",
                  "email": "joao@email.com",
                  "senha": "Senha123",
                  "cpf_cnpj": "123.456.789-09",
                  "telefone": "11987654321",
                  "tipo_usuario": "admin"
                }
            headers:
              - name: Content-Type
                value: application/json
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/usuarios/1/
            name: Inativar Usuário
            meta:
              id: req_9b1cfe5657fa43cdb7e05b2398fa763e
              created: 0
              modified: 1744030485197
              isPrivate: false
              sortKey: -1744022906753
            method: DELETE
            body:
              mimeType: application/json
            headers:
              - name: Content-Type
                value: application/json
                id: pair_b7c2774087784679a8df954737441054
              - id: pair_98bd32fa52b04a74af7cc3ef71daa0cc
                name: Authorization
                value: Bearer
                  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQ0MDMxMjI5fQ.S6Z41L7J35OFmBQ3Wb2aCq5TF5RchKWHiERD7HOyyXo
                disabled: false
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/usuarios/2
            name: Atualizar Dados
            meta:
              id: req_9f5da35337164078b8001c381b18c491
              created: 0
              modified: 1744031075801
              isPrivate: false
              sortKey: -1744022906729
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                  "email": "anovos@email.com",
                	"ativo": true
                }
            headers:
              - name: Content-Type
                value: application/json
                id: pair_629f26c8e6ef48faa11c9ba56c7df2be
              - id: pair_1ee8cfbc54ab494a9f27774092065ec7
                name: Authorization
                value: Bearer
                  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQ0MDMxMjI5fQ.S6Z41L7J35OFmBQ3Wb2aCq5TF5RchKWHiERD7HOyyXo
                disabled: false
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/usuarios/1
            name: Listar Usuários Ativos
            meta:
              id: req_b2fafd30ce1f4086937be127c0e58fe1
              created: 0
              modified: 1744030187430
              isPrivate: false
              sortKey: -1744022906735
            method: GET
            body:
              mimeType: application/json
            headers:
              - name: Content-Type
                value: application/json
                id: pair_0e75f943f6ed4d0fa1c544cc11e31d6d
              - id: pair_9370d10d177940f3a0eb11fe1904fdd4
                name: Authorization
                value: Bearer
                  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQ0MDMxMjI5fQ.S6Z41L7J35OFmBQ3Wb2aCq5TF5RchKWHiERD7HOyyXo
                disabled: false
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Categorias
        meta:
          id: fld_19458550ae3b4449b42f4b30b355cb2e
          created: 1743677695690
          modified: 1743677695690
          sortKey: -1743677695690
        children:
          - url: http://127.0.0.1:8000/api/v1/categorias/
            name: Cadastrar Categoria
            meta:
              id: req_b60a02c5f9be487c9767deea44daaad9
              created: 1743605074850
              modified: 1743679625955
              isPrivate: false
              sortKey: -1743677768256
            method: POST
            body:
              mimeType: application/json
              text: |
                {
                  "nome": "Feminino",
                  "descricao": "Produtos feminino",
                  "imagem_url": "https://example.com/img.jpg",
                  "cor_destaque": "#ff00ff",
                  "ativo": true
                }
            parameters:
              - id: pair_a354fa304b71401bac3633b5f1691412
                disabled: false
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/categorias
            name: Buscar Categorias
            meta:
              id: req_2c67773613084b478b0f169db134ba94
              created: 1743677778856
              modified: 1743765417170
              isPrivate: false
              sortKey: -1743677778856
            method: GET
            headers:
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/categorias/1
            name: Editar Categoria
            meta:
              id: req_8e34557327df4b869c28cc0b53128b61
              created: 1743678105661
              modified: 1743767570421
              isPrivate: false
              sortKey: -1743678105661
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                	"descricao": "Perfumes e produtos para mulheres lindas",
                	"imagem_url": "adicionar imagem"
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/categorias/4/inativar
            name: Inativar/Deletar Categoria
            meta:
              id: req_f427bb3b60d0499ca883080e75aabb2f
              created: 1743678141838
              modified: 1743767455055
              isPrivate: false
              sortKey: -1743678141838
            method: PUT
            headers:
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Produtos
        meta:
          id: fld_dff0a502816748459e8bfe0fe866dc2e
          created: 1743678212946
          modified: 1744126523269
          sortKey: -1743678212946
        children:
          - url: http://127.0.0.1:8000/api/v1/produtos/
            name: Cadastrar Produtos
            meta:
              id: req_a90812f48944431b80e1e4e529624e2f
              created: 1743602857251
              modified: 1744126584061
              isPrivate: false
              sortKey: -1743678218669
            method: POST
            body:
              mimeType: application/json
              text: |-
                {
                  "nome": "csa",
                  "descricao": "casa com GPU dedicada",
                  "preco": 599955.90,
                  "categoria_id": 1
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/produtos
            name: Buscar Produtos
            meta:
              id: req_117becd08bb04cd3bfa66194aca2b654
              created: 1743679904060
              modified: 1743775464726
              isPrivate: false
              sortKey: -1743678218769
            method: GET
            headers:
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/produtos/10/inativar
            name: Inativar/Deletar Produto
            meta:
              id: req_8fb308f26b654df8ba1b59bd3f0fc188
              created: 1743765839874
              modified: 1743769412046
              isPrivate: false
              sortKey: -1743678218869
            method: PUT
            headers:
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/produtos/2/editar
            name: Editar Produto
            meta:
              id: req_ea9f05e29c494c6e8357394bae9e8a40
              created: 1743767557723
              modified: 1744128174785
              isPrivate: false
              sortKey: -1743678218819
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                	"margem_lucro": 25,
                	"preco":1000
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Estoque
        meta:
          id: fld_141b389e35e8480b9aa59dc7933c6cb7
          created: 1743772535080
          modified: 1744127031793
          sortKey: -1743772535080
        children:
          - url: http://127.0.0.1:8000/api/v1/estoque/
            name: Cadastrar Estoque
            meta:
              id: req_37f806f1fa294dfba6151afd29c7d06c
              created: 1743772541780
              modified: 1744128148463
              isPrivate: false
              sortKey: -1743772541780
            method: POST
            body:
              mimeType: application/json
              text: |
                {
                  "produto_id": 2,
                  "quantidade": 20
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/estoque/11
            name: Editar Estoque
            meta:
              id: req_5c77c2c9f8e8415287d08d64f08fe940
              created: 1743772555573
              modified: 1743773331606
              isPrivate: false
              sortKey: -1743725380324.5
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                  "quantidade": 10
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/estoque/11
            name: Deletar Estoque
            meta:
              id: req_07d0f2d51b7247d191413860c4afbffc
              created: 1743772579937
              modified: 1743773364468
              isPrivate: false
              sortKey: -1743701799596.75
            method: DELETE
            headers:
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/estoque/
            name: Listar Estoque
            meta:
              id: req_6475e66c84254b8fba2831feca2e69fc
              created: 1743772609851
              modified: 1743773374952
              isPrivate: false
              sortKey: -1743772609851
            method: GET
            headers:
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Cupom
        meta:
          id: fld_f972a789b1064cd394b9013b65fd1323
          created: 1743774020461
          modified: 1743774020461
          sortKey: -1743774020461
        children:
          - url: http://127.0.0.1:8000/api/v1/cupons/DESCONTO10
            name: Listar Cupom
            meta:
              id: req_f041a6a54fd54f209ea7e35861d015fa
              created: 1743774037695
              modified: 1743776502590
              isPrivate: false
              sortKey: -1743776488505
            method: GET
            headers:
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/cupons/
            name: Cadastrar Cupom
            meta:
              id: req_1f4b488915d84f16acd3daaa3a615186
              created: 1743774044025
              modified: 1743776503780
              isPrivate: false
              sortKey: -1743776488492.5
            method: POST
            body:
              mimeType: application/json
              text: |-
                {
                  "codigo": "DESCONTO10",
                  "desconto": 10.0,
                  "validade": "2025-12-31T23:59:59",
                  "ativo": true
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/cupons/1
            name: Editar Cupom por Id
            meta:
              id: req_7a41fa0f24af44e9bb01a138c95657e1
              created: 1743774051232
              modified: 1743776495045
              isPrivate: false
              sortKey: -1743776488580
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                  "codigo": "DESCONTO10",
                  "desconto": 10.0
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/cupons/1/desativar
            name: Desativar Cupom
            meta:
              id: req_7cd0135cdffe45a289b93a29845ea049
              created: 1743774060205
              modified: 1743776501493
              isPrivate: false
              sortKey: -1743776488530
            method: PUT
            headers:
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/cupons/codigo/DESCONTO10
            name: Editar Cupom por Codigo
            meta:
              id: req_18c6720f3afa483ba7e54b63d27c4699
              created: 1743775122654
              modified: 1743776488588
              isPrivate: false
              sortKey: -1743776488480
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                  "codigo": "DESCONTO10",
                  "desconto": 25
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Autenticacao
        meta:
          id: fld_d68732376b4548d083f1d0e8b7312d81
          created: 1743775513390
          modified: 1743775513390
          sortKey: -1743775513390
        children:
          - url: http://127.0.0.1:8000/auth/register/
            name: register
            meta:
              id: req_0dfe2a91942842b09e3bda6a2dbbf2ae
              created: 1743601059890
              modified: 1744022424096
              isPrivate: false
              sortKey: -1743775521723
            method: POST
            body:
              mimeType: application/json
              text: |
                {
                  "nome": "João Silva",
                  "email": "josao@email.com",
                  "senha": "Senha123",
                  "cpf_cnpj": "123.456.789-09",
                  "telefone": "11987654321",
                  "tipo_usuario": "admin"
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/auth/login
            name: login
            meta:
              id: req_1074713839b4485284add545e9cfcbaa
              created: 1743601564489
              modified: 1744030654060
              isPrivate: false
              sortKey: -1743775521823
            method: POST
            body:
              mimeType: application/json
              text: |
                {
                  "email": "josao@email.com",
                  "senha": "Senha123"
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.1
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Promocoes
        meta:
          id: fld_18f533342b184f69be5f525d78c5cd80
          created: 1743776459948
          modified: 1743776459948
          sortKey: -1743776459948
      - name: Promocao
        meta:
          id: fld_ee5404d7b6c9423aba7fe9d33d259445
          created: 1743776513737
          modified: 1743776513737
          sortKey: -1743725374013
        children:
          - url: http://127.0.0.1:8000/api/v1/promocoes
            name: Cadastrar Promocao
            meta:
              id: req_9c9f91917a8a4d5792f979e16fe98525
              created: 1743776513738
              modified: 1743777250178
              isPrivate: false
              sortKey: -1743772541780
            method: POST
            body:
              mimeType: application/json
              text: |
                {
                  "produto_id": 11,
                  "desconto_percentual": 15.00,
                  "preco_promocional": 70.00,
                  "data_inicio": "2025-05-06T00:00:00",
                  "data_fim": "2025-06-06T23:59:59",
                  "ativo": true
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/promocoes/6/editar
            name: Editar Promocao
            meta:
              id: req_ed7da4dbaaf4427997eb74796c62f888
              created: 1743776513740
              modified: 1743777533656
              isPrivate: false
              sortKey: -1743725380324.5
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                  "desconto_percentual": 15.00,
                  "preco_promocional": 70.00
                }
            headers:
              - name: Content-Type
                value: application/json
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/promocoes/6/inativar/
            name: Desativar Promocao
            meta:
              id: req_842ccec142a244eca5fbd7c966c1d216
              created: 1743776513741
              modified: 1743777652595
              isPrivate: false
              sortKey: -1743701799596.75
            method: PUT
            headers:
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/promocoes/6
            name: Listar Promocoes
            meta:
              id: req_3f2ef89d8264461aa8b0faa5da2ce076
              created: 1743776513742
              modified: 1743777267445
              isPrivate: false
              sortKey: -1743772609851
            method: GET
            headers:
              - name: User-Agent
                value: insomnia/11.0.2
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Venda
        meta:
          id: fld_bf2fa02d1846458e9098da1261176a8f
          created: 1744119675933
          modified: 1744119675933
          sortKey: -1744119675933
        children:
          - url: http://127.0.0.1:8000/api/v1/vendas/
            name: Criar Venda
            meta:
              id: req_6cb8730c614a42068a9060ec46a9883f
              created: 1744119666509
              modified: 1744128207762
              isPrivate: false
              sortKey: -1744119678865
            method: POST
            body:
              mimeType: application/json
              text: |
                {
                  "endereco_id": 1,
                  "cupom_id": 1,
                  "itens": [
                    {
                      "produto_id": 2,
                      "quantidade": 1
                    }
                  ]
                }
            headers:
              - name: Content-Type
                value: application/json
                id: pair_fb33e4297c3d4f7398351edd49fda62f
              - name: Authorization
                value: Bearer
                  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ0MTI5NDEwfQ.yZJ-pUIvA0geSKchrWZIW9tcWvZJZ6vyrFRVMTb8lFI
                id: pair_8c82d3da40f940b48641b4c4950de1f3
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/venda/1
            name: Listar Vendas do Usuário
            meta:
              id: req_68cc2275004c4b18825f615fe2f2c6a7
              created: 1744119666518
              modified: 1744122768324
              isPrivate: false
              sortKey: -1744119678965
            method: GET
            headers:
              - name: Authorization
                value: Bearer {{ token }}
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/vendas/8
            name: Detalhar Venda
            meta:
              id: req_12fa4551babc43e7a98e73b2fa215660
              created: 1744119666524
              modified: 1744129576536
              isPrivate: false
              sortKey: -1744119679065
            method: GET
            body:
              mimeType: application/json
            headers:
              - name: Content-Type
                value: application/json
                id: pair_205eb828e77a438b90e83b9d78bbeb55
              - name: Authorization
                value: Bearer
                  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzQ0MTMxMzY4fQ.gtV84XaHygjfsJ0BTfCU31J364vLDdPt7rvqHSQbbNw
                id: pair_243648c101a84685aea4dc4261ef6354
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: "{{ base_url }}/vendas/1"
            name: Cancelar Venda
            meta:
              id: req_c991dd231f664131a63e574ad58cd728
              created: 1744119666528
              modified: 1744119684387
              isPrivate: false
              sortKey: -1744119679015
            method: DELETE
            headers:
              - name: Authorization
                value: Bearer {{ token }}
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
      - name: Endereços
        meta:
          id: fld_a43e727f698b4f27b89e9c019c8e363d
          created: 1744126357378
          modified: 1744126360836
          sortKey: -1744119676033
        children:
          - url: http://127.0.0.1:8000/api/v1/endereco
            name: Criar Endereço
            meta:
              id: req_9145561d0b9d4de182cd9da64b03ac8c
              created: 1744126357380
              modified: 1744126404108
              isPrivate: false
              sortKey: -1744126357380
            method: POST
            body:
              mimeType: application/json
              text: |-
                {
                  "usuario_id": 1,
                  "logradouro": "Rua das Flores",
                  "numero": "123",
                  "complemento": "Apto 101",
                  "bairro": "Centro",
                  "cidade": "Cidade",
                  "estado": "SP",
                  "cep": "12345-678"
                }
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: http://127.0.0.1:8000/api/v1/endereco/1
            name: Listar Endereços
            meta:
              id: req_f187fae030694592a7ba615bc41f7e43
              created: 1744126357382
              modified: 1744126389112
              isPrivate: false
              sortKey: -1744126357382
            method: GET
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: "{{ base_url }}/1"
            name: Buscar Endereço por ID
            meta:
              id: req_5b9b5754bc3040009ceb13611b2ded8b
              created: 1744126357383
              modified: 1744126357383
              isPrivate: false
              sortKey: -1744126357383
            method: GET
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: "{{ base_url }}/1/editar"
            name: Atualizar Endereço
            meta:
              id: req_7f0a7ec0e70c486b99e9554c9c0f4d4f
              created: 1744126357384
              modified: 1744126357384
              isPrivate: false
              sortKey: -1744126357384
            method: PUT
            body:
              mimeType: application/json
              text: |-
                {
                  "logradouro": "Rua Nova",
                  "numero": "456",
                  "complemento": "Casa",
                  "bairro": "Jardins",
                  "cidade": "Nova Cidade",
                  "estado": "RJ",
                  "cep": "98765-432"
                }
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
          - url: "{{ base_url }}/1/inativar"
            name: Inativar Endereço
            meta:
              id: req_3743d80f72604dc592ac7c47d677ec0a
              created: 1744126357385
              modified: 1744126357385
              isPrivate: false
              sortKey: -1744126357385
            method: DELETE
            settings:
              renderRequestBody: true
              encodeUrl: true
              followRedirects: global
              cookies:
                send: true
                store: true
              rebuildPath: true
cookieJar:
  name: Default Jar
  meta:
    id: jar_99d30891da4bdcebc63947a8fc17f076de878684
    created: 1706532558533
    modified: 1743169435415
  cookies:
    - key: JSESSIONID
      value: A9720FF77E9F05B738F4E14CFF81F4F9
      domain: localhost
      path: /
      httpOnly: true
      hostOnly: true
      creation: 2024-04-18T13:37:19.220Z
      lastAccessed: 2024-04-18T13:37:19.220Z
      id: 7fa98f99-fc11-410d-a91e-0d9350afb32b
    - key: JSESSIONID
      value: A9720FF77E9F05B738F4E14CFF81F4F9.cge_prodesk_04
      domain: localhost
      path: /controleinterno
      hostOnly: true
      creation: 2024-05-07T12:53:39.132Z
      lastAccessed: 2024-05-07T12:53:39.132Z
      id: 56abeadd-3145-4746-bca2-52e054ce26ac
    - key: csrftoken
      value: Bg7E5xJo9h2SITjrBzFuDqGzwzIRaLQs
      maxAge: 31449600
      domain: 127.0.0.1
      path: /
      hostOnly: true
      creation: 2024-10-22T11:27:47.051Z
      lastAccessed: 2024-10-22T11:32:33.614Z
      sameSite: lax
      id: 22b26271-440a-4aed-af8c-0096c47ea107
    - key: access_token
      value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNzQ1NTU3LCJpYXQiOjE3NDA3NDE5NTcsImp0aSI6ImJkNDlhODE3NDZjMzRmOWU5NmI3N2RjNDFkY2VhYWUxIiwidXNlcl9pZCI6MX0.YuBuM6JDYx_fP1O78GtLv07MC5RYinHzZ7QhSragFtw
      domain: 127.0.0.1
      path: /
      secure: true
      httpOnly: true
      hostOnly: true
      creation: 2025-02-26T14:25:01.225Z
      lastAccessed: 2025-02-28T11:25:57.398Z
      sameSite: strict
      id: a17a3a42-e4c5-40bd-be36-6078dc07c276
    - key: JSESSIONID
      value: atiseip-app1
      domain: sei.pi.gov.br
      path: /
      hostOnly: true
      creation: 2025-03-28T13:43:55.414Z
      lastAccessed: 2025-03-28T13:43:55.414Z
      id: a75c7533-6672-4802-9341-539c572faa03
environments:
  name: Base Environment
  meta:
    id: env_99d30891da4bdcebc63947a8fc17f076de878684
    created: 1706532558530
    modified: 1738587956453
    isPrivate: false
  subEnvironments:
    - name: sei
      meta:
        id: env_778f20a80fde44b08157d9fab1002ea6
        created: 1738587953534
        modified: 1739269571582
        isPrivate: false
        sortKey: 1738587953534
      data:
        base_url: https://dev.api.sead.pi.gov.br/sei/v1
        usuario: fabianolira@cge.pi.gov.br
        senha: fab231282aila
        orgao: CGE-PI
        token: ZDczODQ4OTk5YmM3NzVmYjU5NzQwNmM0NGQwN2MzYjZhNGNiYjhhZmJWbzJaR3h3TmxKclNrOVhhbG8yTDI1S2FXRXdXU3RYTUZwcFVXbGtSMlJxVVQwOWZIeHRXalprZW1ONlQzcGpaazV1Y0dGVWJtYzlQWHg4Tlh4OA==
    - name: New Environment
      meta:
        id: env_d3ec1e6bf3df43a1be17bdcda87cf59e
        created: 1740652674567
        modified: 1740652674567
        isPrivate: false
        sortKey: 1740652674567
