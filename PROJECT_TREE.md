]633;E;echo '```text';47cab9b4-aeea-4f48-928c-bada9f8a6e19]633;C```text
.
├── .env
├── .env.example
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pytest_cache
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v
│       └── cache
│           ├── lastfailed
│           └── nodeids
├── AI_PROMPTS_DISCLOSURE.md
├── PHASE_5_1_REMEDIATION_REPORT.md
├── PHASE_5_2_COMPLETION_REPORT.md
├── PROJECT_TREE.md
├── README.md
├── backend
│   ├── .pytest_cache
│   │   ├── .gitignore
│   │   ├── CACHEDIR.TAG
│   │   ├── README.md
│   │   └── v
│   │       └── cache
│   │           ├── lastfailed
│   │           └── nodeids
│   ├── Dockerfile
│   ├── MIGRATIONS.md
│   ├── SECURITY.md
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 0001_initial_schema.py
│   │       ├── 0002_financial_precision_and_date_types.py
│   │       ├── 0003_hybrid_search_indexes.py
│   │       ├── 0004_cross_verification_history.py
│   │       ├── 0005_task_outbox.py
│   │       ├── 0006_security_owner_scope.py
│   │       ├── 0007_worker_lease_and_currency.py
│   │       ├── 0008_drop_currency_default.py
│   │       └── 0009_lease_epoch_fencing.py
│   ├── alembic.ini
│   ├── api
│   │   └── routes
│   │       ├── auth.py
│   │       ├── corrections.py
│   │       ├── documents.py
│   │       └── search.py
│   ├── core
│   │   ├── celery_app.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── rate_limit.py
│   │   └── security.py
│   ├── evaluation
│   ├── main.py
│   ├── models
│   │   ├── document.py
│   │   └── schemas.py
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── services
│   │   ├── ai_extractor.py
│   │   ├── cross_verification_service.py
│   │   ├── document_parser.py
│   │   ├── file_security.py
│   │   ├── outbox_service.py
│   │   ├── validator.py
│   │   └── vector_service.py
│   ├── tasks
│   │   └── processing_tasks.py
│   └── tests
│       ├── test_api.py
│       ├── test_celery_retry.py
│       ├── test_concurrency_and_reliability.py
│       ├── test_cross_verification.py
│       ├── test_duplicates.py
│       ├── test_evaluation_suite.py
│       ├── test_financial_precision.py
│       ├── test_ghr_01_02_03.py
│       ├── test_ghr_04_05_07_08.py
│       ├── test_hotfix_batch_a.py
│       ├── test_hybrid_search.py
│       ├── test_large_pdf_and_ai.py
│       ├── test_migrations.py
│       ├── test_parser.py
│       ├── test_search_indexes.py
│       ├── test_security.py
│       ├── test_upload_security.py
│       └── test_validator.py
├── backup_before_migration.sql
├── docker-compose.prod.yml
├── docker-compose.yml
├── evaluation
│   ├── benchmark_dataset
│   │   ├── dataset_manifest.json
│   │   ├── files
│   │   │   ├── 01_digital_standard.pdf
│   │   │   ├── 02_multipage_12pages.pdf
│   │   │   ├── 03_scanned_clean.pdf
│   │   │   ├── 04_scanned_skewed_noisy.pdf
│   │   │   ├── 05_receipt_clean.png
│   │   │   ├── 06_invoice_poor_photo.jpg
│   │   │   ├── 07_multisheet_workbook.xlsx
│   │   │   ├── 08_services_invoice.csv
│   │   │   ├── 09_incomplete_null_fields.pdf
│   │   │   └── 10_math_discrepancy.pdf
│   │   ├── large_pdf_files
│   │   │   ├── scale_test_1000pages.pdf
│   │   │   ├── scale_test_100pages.pdf
│   │   │   └── scale_test_500pages.pdf
│   │   └── sample_invoices.json
│   ├── benchmark_large_pdf.py
│   ├── evaluate.py
│   ├── evaluation_report.md
│   ├── generate_dataset.py
│   └── large_pdf_benchmark_report.md
├── frontend
│   ├── .env.example
│   ├── .env.local
│   ├── .next
│   │   ├── BUILD_ID
│   │   ├── app-build-manifest.json
│   │   ├── app-path-routes-manifest.json
│   │   ├── build-manifest.json
│   │   ├── cache
│   │   │   ├── .tsbuildinfo
│   │   │   ├── config.json
│   │   │   ├── swc
│   │   │   │   └── plugins
│   │   │   │       └── v7_linux_x86_64_0.106.15
│   │   │   └── webpack
│   │   │       ├── client-development
│   │   │       │   ├── 0.pack.gz
│   │   │       │   ├── 1.pack.gz
│   │   │       │   ├── 2.pack.gz
│   │   │       │   ├── 3.pack.gz
│   │   │       │   ├── 4.pack.gz
│   │   │       │   ├── 5.pack.gz
│   │   │       │   ├── 6.pack.gz
│   │   │       │   ├── 7.pack.gz
│   │   │       │   ├── 8.pack.gz
│   │   │       │   ├── 9.pack.gz
│   │   │       │   ├── index.pack.gz
│   │   │       │   └── index.pack.gz.old
│   │   │       ├── client-development-fallback
│   │   │       │   ├── 0.pack.gz
│   │   │       │   └── index.pack.gz
│   │   │       ├── client-production
│   │   │       │   ├── 0.pack
│   │   │       │   ├── 1.pack
│   │   │       │   ├── 2.pack
│   │   │       │   ├── 3.pack
│   │   │       │   ├── 4.pack
│   │   │       │   ├── 5.pack
│   │   │       │   ├── 6.pack
│   │   │       │   ├── 7.pack
│   │   │       │   ├── 8.pack
│   │   │       │   ├── index.pack
│   │   │       │   └── index.pack.old
│   │   │       ├── edge-server-production
│   │   │       │   ├── 0.pack
│   │   │       │   └── index.pack
│   │   │       ├── server-development
│   │   │       │   ├── 0.pack.gz
│   │   │       │   ├── 1.pack.gz
│   │   │       │   ├── 2.pack.gz
│   │   │       │   ├── 3.pack.gz
│   │   │       │   ├── 4.pack.gz
│   │   │       │   ├── 5.pack.gz
│   │   │       │   ├── index.pack.gz
│   │   │       │   └── index.pack.gz.old
│   │   │       └── server-production
│   │   │           ├── 0.pack
│   │   │           ├── 1.pack
│   │   │           ├── 2.pack
│   │   │           ├── 3.pack
│   │   │           ├── 4.pack
│   │   │           ├── index.pack
│   │   │           └── index.pack.old
│   │   ├── export-marker.json
│   │   ├── images-manifest.json
│   │   ├── next-minimal-server.js.nft.json
│   │   ├── next-server.js.nft.json
│   │   ├── package.json
│   │   ├── prerender-manifest.json
│   │   ├── react-loadable-manifest.json
│   │   ├── required-server-files.json
│   │   ├── routes-manifest.json
│   │   ├── server
│   │   │   ├── app
│   │   │   │   ├── _not-found
│   │   │   │   │   ├── page.js
│   │   │   │   │   ├── page.js.nft.json
│   │   │   │   │   └── page_client-reference-manifest.js
│   │   │   │   ├── _not-found.html
│   │   │   │   ├── _not-found.meta
│   │   │   │   ├── _not-found.rsc
│   │   │   │   ├── documents
│   │   │   │   │   └── [id]
│   │   │   │   │       ├── page.js
│   │   │   │   │       ├── page.js.nft.json
│   │   │   │   │       └── page_client-reference-manifest.js
│   │   │   │   ├── index.html
│   │   │   │   ├── index.meta
│   │   │   │   ├── index.rsc
│   │   │   │   ├── page.js
│   │   │   │   ├── page.js.nft.json
│   │   │   │   ├── page_client-reference-manifest.js
│   │   │   │   ├── search
│   │   │   │   │   ├── page.js
│   │   │   │   │   ├── page.js.nft.json
│   │   │   │   │   └── page_client-reference-manifest.js
│   │   │   │   ├── search.html
│   │   │   │   ├── search.meta
│   │   │   │   └── search.rsc
│   │   │   ├── app-paths-manifest.json
│   │   │   ├── chunks
│   │   │   │   ├── 181.js
│   │   │   │   ├── 682.js
│   │   │   │   └── font-manifest.json
│   │   │   ├── font-manifest.json
│   │   │   ├── functions-config-manifest.json
│   │   │   ├── interception-route-rewrite-manifest.js
│   │   │   ├── middleware-build-manifest.js
│   │   │   ├── middleware-manifest.json
│   │   │   ├── middleware-react-loadable-manifest.js
│   │   │   ├── next-font-manifest.js
│   │   │   ├── next-font-manifest.json
│   │   │   ├── pages
│   │   │   │   ├── 404.html
│   │   │   │   ├── 500.html
│   │   │   │   ├── _app.js
│   │   │   │   ├── _app.js.nft.json
│   │   │   │   ├── _document.js
│   │   │   │   ├── _document.js.nft.json
│   │   │   │   ├── _error.js
│   │   │   │   └── _error.js.nft.json
│   │   │   ├── pages-manifest.json
│   │   │   ├── server-reference-manifest.js
│   │   │   ├── server-reference-manifest.json
│   │   │   └── webpack-runtime.js
│   │   ├── static
│   │   │   ├── TCu7Jnv_u7qpcMCkGZfcf
│   │   │   │   ├── _buildManifest.js
│   │   │   │   └── _ssgManifest.js
│   │   │   ├── chunks
│   │   │   │   ├── 117-78d466e9c4558ff6.js
│   │   │   │   ├── 142-82e3fb94bb2082a6.js
│   │   │   │   ├── 648-8b1c779413e524de.js
│   │   │   │   ├── 679-0d014afab13973e6.js
│   │   │   │   ├── app
│   │   │   │   │   ├── _not-found
│   │   │   │   │   │   └── page-756e6e8a259ba367.js
│   │   │   │   │   ├── documents
│   │   │   │   │   │   └── [id]
│   │   │   │   │   │       └── page-1f3aef851d0bd20c.js
│   │   │   │   │   ├── layout-c1e06e3735f5593b.js
│   │   │   │   │   ├── page-69592fcfe8c978ca.js
│   │   │   │   │   └── search
│   │   │   │   │       └── page-b1b5e19ac3da8c8e.js
│   │   │   │   ├── fd9d1056-cce117dc4e21e608.js
│   │   │   │   ├── framework-f66176bb897dc684.js
│   │   │   │   ├── main-2a2e48493bee7cc3.js
│   │   │   │   ├── main-app-06330196d14a8bfe.js
│   │   │   │   ├── pages
│   │   │   │   │   ├── _app-72b849fbd24ac258.js
│   │   │   │   │   └── _error-7ba65e1336b92748.js
│   │   │   │   ├── polyfills-42372ed130431b0a.js
│   │   │   │   └── webpack-03f7c6bc932ce1e3.js
│   │   │   └── css
│   │   │       └── accf655cf8846a23.css
│   │   ├── trace
│   │   └── types
│   │       ├── app
│   │       │   ├── documents
│   │       │   │   └── [id]
│   │       │   │       └── page.ts
│   │       │   ├── layout.ts
│   │       │   ├── page.ts
│   │       │   └── search
│   │       │       └── page.ts
│   │       └── package.json
│   ├── app
│   │   ├── documents
│   │   │   └── [id]
│   │   │       └── page.tsx
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── search
│   │       └── page.tsx
│   ├── components
│   │   ├── FileUploader.tsx
│   │   ├── Navbar.tsx
│   │   ├── StatusBadge.tsx
│   │   └── ValidationAlerts.tsx
│   ├── lib
│   │   ├── api.ts
│   │   └── money.ts
│   ├── next-env.d.ts
│   ├── next.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
├── pytest.ini
└── venv
    ├── .gitignore
    ├── bin
    │   ├── Activate.ps1
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── alembic
    │   ├── celery
    │   ├── distro
    │   ├── dotenv
    │   ├── f2py
    │   ├── fastapi
    │   ├── hf
    │   ├── httpx
    │   ├── httpx2
    │   ├── huggingface-cli
    │   ├── idna
    │   ├── mako-render
    │   ├── normalizer
    │   ├── numpy-config
    │   ├── onnxruntime_test
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.14
    │   ├── py.test
    │   ├── pygmentize
    │   ├── pymupdf
    │   ├── pymupdf-config
    │   ├── pytesseract
    │   ├── pytest
    │   ├── python -> python3
    │   ├── python3 -> /home/codespace/.python/current/bin/python3
    │   ├── python3.14 -> python3
    │   ├── tabulate
    │   ├── tiny-agents
    │   ├── tqdm
    │   ├── uvicorn
    │   ├── watchfiles
    │   ├── websockets
    │   └── 𝜋thon -> python3
    ├── include
    │   └── site
    │       └── python3.14
    │           └── greenlet
    │               └── greenlet.h
    ├── lib
    │   └── python3.14
    │       └── site-packages
    │           ├── PIL
    │           │   ├── AvifImagePlugin.py
    │           │   ├── BdfFontFile.py
    │           │   ├── BlpImagePlugin.py
    │           │   ├── BmpImagePlugin.py
    │           │   ├── BufrStubImagePlugin.py
    │           │   ├── ContainerIO.py
    │           │   ├── CurImagePlugin.py
    │           │   ├── DcxImagePlugin.py
    │           │   ├── DdsImagePlugin.py
    │           │   ├── EpsImagePlugin.py
    │           │   ├── ExifTags.py
    │           │   ├── FitsImagePlugin.py
    │           │   ├── FliImagePlugin.py
    │           │   ├── FontFile.py
    │           │   ├── FpxImagePlugin.py
    │           │   ├── FtexImagePlugin.py
    │           │   ├── GbrImagePlugin.py
    │           │   ├── GdImageFile.py
    │           │   ├── GifImagePlugin.py
    │           │   ├── GimpGradientFile.py
    │           │   ├── GimpPaletteFile.py
    │           │   ├── GribStubImagePlugin.py
    │           │   ├── Hdf5StubImagePlugin.py
    │           │   ├── IcnsImagePlugin.py
    │           │   ├── IcoImagePlugin.py
    │           │   ├── ImImagePlugin.py
    │           │   ├── Image.py
    │           │   ├── ImageChops.py
    │           │   ├── ImageCms.py
    │           │   ├── ImageColor.py
    │           │   ├── ImageDraw.py
    │           │   ├── ImageDraw2.py
    │           │   ├── ImageEnhance.py
    │           │   ├── ImageFile.py
    │           │   ├── ImageFilter.py
    │           │   ├── ImageFont.py
    │           │   ├── ImageGrab.py
    │           │   ├── ImageMath.py
    │           │   ├── ImageMode.py
    │           │   ├── ImageMorph.py
    │           │   ├── ImageOps.py
    │           │   ├── ImagePalette.py
    │           │   ├── ImagePath.py
    │           │   ├── ImageQt.py
    │           │   ├── ImageSequence.py
    │           │   ├── ImageShow.py
    │           │   ├── ImageStat.py
    │           │   ├── ImageText.py
    │           │   ├── ImageTk.py
    │           │   ├── ImageTransform.py
    │           │   ├── ImageWin.py
    │           │   ├── ImtImagePlugin.py
    │           │   ├── IptcImagePlugin.py
    │           │   ├── Jpeg2KImagePlugin.py
    │           │   ├── JpegImagePlugin.py
    │           │   ├── JpegPresets.py
    │           │   ├── McIdasImagePlugin.py
    │           │   ├── MicImagePlugin.py
    │           │   ├── MpegImagePlugin.py
    │           │   ├── MpoImagePlugin.py
    │           │   ├── MspImagePlugin.py
    │           │   ├── PSDraw.py
    │           │   ├── PaletteFile.py
    │           │   ├── PalmImagePlugin.py
    │           │   ├── PcdImagePlugin.py
    │           │   ├── PcfFontFile.py
    │           │   ├── PcxImagePlugin.py
    │           │   ├── PdfImagePlugin.py
    │           │   ├── PdfParser.py
    │           │   ├── PixarImagePlugin.py
    │           │   ├── PngImagePlugin.py
    │           │   ├── PpmImagePlugin.py
    │           │   ├── PsdImagePlugin.py
    │           │   ├── QoiImagePlugin.py
    │           │   ├── SgiImagePlugin.py
    │           │   ├── SpiderImagePlugin.py
    │           │   ├── SunImagePlugin.py
    │           │   ├── TarIO.py
    │           │   ├── TgaImagePlugin.py
    │           │   ├── TiffImagePlugin.py
    │           │   ├── TiffTags.py
    │           │   ├── WalImageFile.py
    │           │   ├── WebPImagePlugin.py
    │           │   ├── WmfImagePlugin.py
    │           │   ├── XVThumbImagePlugin.py
    │           │   ├── XbmImagePlugin.py
    │           │   ├── XpmImagePlugin.py
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _avif.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _avif.pyi
    │           │   ├── _binary.py
    │           │   ├── _deprecate.py
    │           │   ├── _imaging.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _imaging.pyi
    │           │   ├── _imagingcms.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _imagingcms.pyi
    │           │   ├── _imagingft.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _imagingft.pyi
    │           │   ├── _imagingmath.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _imagingmath.pyi
    │           │   ├── _imagingmorph.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _imagingmorph.pyi
    │           │   ├── _imagingtk.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _imagingtk.pyi
    │           │   ├── _tkinter_finder.py
    │           │   ├── _typing.py
    │           │   ├── _util.py
    │           │   ├── _version.py
    │           │   ├── _webp.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _webp.pyi
    │           │   ├── features.py
    │           │   ├── py.typed
    │           │   └── report.py
    │           ├── _pytest
    │           │   ├── __init__.py
    │           │   ├── _argcomplete.py
    │           │   ├── _code
    │           │   │   ├── __init__.py
    │           │   │   ├── code.py
    │           │   │   └── source.py
    │           │   ├── _io
    │           │   │   ├── __init__.py
    │           │   │   ├── pprint.py
    │           │   │   ├── saferepr.py
    │           │   │   ├── terminalwriter.py
    │           │   │   └── wcwidth.py
    │           │   ├── _py
    │           │   │   ├── __init__.py
    │           │   │   ├── error.py
    │           │   │   └── path.py
    │           │   ├── _version.py
    │           │   ├── approx.py
    │           │   ├── assertion
    │           │   │   ├── __init__.py
    │           │   │   ├── _compare_any.py
    │           │   │   ├── _compare_mapping.py
    │           │   │   ├── _compare_sequence.py
    │           │   │   ├── _compare_set.py
    │           │   │   ├── _guards.py
    │           │   │   ├── _typing.py
    │           │   │   ├── compare_text.py
    │           │   │   ├── highlight.py
    │           │   │   ├── rewrite.py
    │           │   │   ├── truncate.py
    │           │   │   └── util.py
    │           │   ├── cacheprovider.py
    │           │   ├── capture.py
    │           │   ├── compat.py
    │           │   ├── config
    │           │   │   ├── __init__.py
    │           │   │   ├── argparsing.py
    │           │   │   ├── exceptions.py
    │           │   │   └── findpaths.py
    │           │   ├── debugging.py
    │           │   ├── deprecated.py
    │           │   ├── doctest.py
    │           │   ├── faulthandler.py
    │           │   ├── fixtures.py
    │           │   ├── freeze_support.py
    │           │   ├── helpconfig.py
    │           │   ├── hookspec.py
    │           │   ├── junitxml.py
    │           │   ├── legacypath.py
    │           │   ├── logging.py
    │           │   ├── main.py
    │           │   ├── mark
    │           │   │   ├── __init__.py
    │           │   │   ├── expression.py
    │           │   │   └── structures.py
    │           │   ├── monkeypatch.py
    │           │   ├── nodeid.py
    │           │   ├── nodes.py
    │           │   ├── outcomes.py
    │           │   ├── pastebin.py
    │           │   ├── pathlib.py
    │           │   ├── py.typed
    │           │   ├── pytester.py
    │           │   ├── pytester_assertions.py
    │           │   ├── python.py
    │           │   ├── raises.py
    │           │   ├── recwarn.py
    │           │   ├── reports.py
    │           │   ├── runner.py
    │           │   ├── scope.py
    │           │   ├── setuponly.py
    │           │   ├── setupplan.py
    │           │   ├── skipping.py
    │           │   ├── stash.py
    │           │   ├── stepwise.py
    │           │   ├── subtests.py
    │           │   ├── terminal.py
    │           │   ├── terminalprogress.py
    │           │   ├── threadexception.py
    │           │   ├── timing.py
    │           │   ├── tmpdir.py
    │           │   ├── tracemalloc.py
    │           │   ├── unittest.py
    │           │   ├── unraisableexception.py
    │           │   ├── warning_types.py
    │           │   └── warnings.py
    │           ├── _yaml
    │           │   └── __init__.py
    │           ├── alembic
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── autogenerate
    │           │   │   ├── __init__.py
    │           │   │   ├── api.py
    │           │   │   ├── compare
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── comments.py
    │           │   │   │   ├── constraints.py
    │           │   │   │   ├── schema.py
    │           │   │   │   ├── server_defaults.py
    │           │   │   │   ├── tables.py
    │           │   │   │   ├── types.py
    │           │   │   │   └── util.py
    │           │   │   ├── render.py
    │           │   │   └── rewriter.py
    │           │   ├── command.py
    │           │   ├── config.py
    │           │   ├── context.py
    │           │   ├── context.pyi
    │           │   ├── ddl
    │           │   │   ├── __init__.py
    │           │   │   ├── _autogen.py
    │           │   │   ├── base.py
    │           │   │   ├── impl.py
    │           │   │   ├── mssql.py
    │           │   │   ├── mysql.py
    │           │   │   ├── oracle.py
    │           │   │   ├── postgresql.py
    │           │   │   └── sqlite.py
    │           │   ├── environment.py
    │           │   ├── ext
    │           │   │   ├── __init__.py
    │           │   │   └── checkconstraint_byname.py
    │           │   ├── migration.py
    │           │   ├── op.py
    │           │   ├── op.pyi
    │           │   ├── operations
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── batch.py
    │           │   │   ├── ops.py
    │           │   │   ├── schemaobj.py
    │           │   │   └── toimpl.py
    │           │   ├── py.typed
    │           │   ├── runtime
    │           │   │   ├── __init__.py
    │           │   │   ├── environment.py
    │           │   │   ├── migration.py
    │           │   │   └── plugins.py
    │           │   ├── script
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── revision.py
    │           │   │   └── write_hooks.py
    │           │   ├── templates
    │           │   │   ├── async
    │           │   │   │   ├── README
    │           │   │   │   ├── alembic.ini.mako
    │           │   │   │   ├── env.py
    │           │   │   │   └── script.py.mako
    │           │   │   ├── generic
    │           │   │   │   ├── README
    │           │   │   │   ├── alembic.ini.mako
    │           │   │   │   ├── env.py
    │           │   │   │   └── script.py.mako
    │           │   │   ├── multidb
    │           │   │   │   ├── README
    │           │   │   │   ├── alembic.ini.mako
    │           │   │   │   ├── env.py
    │           │   │   │   └── script.py.mako
    │           │   │   ├── pyproject
    │           │   │   │   ├── README
    │           │   │   │   ├── alembic.ini.mako
    │           │   │   │   ├── env.py
    │           │   │   │   ├── pyproject.toml.mako
    │           │   │   │   └── script.py.mako
    │           │   │   └── pyproject_async
    │           │   │       ├── README
    │           │   │       ├── alembic.ini.mako
    │           │   │       ├── env.py
    │           │   │       ├── pyproject.toml.mako
    │           │   │       └── script.py.mako
    │           │   ├── testing
    │           │   │   ├── __init__.py
    │           │   │   ├── assertions.py
    │           │   │   ├── env.py
    │           │   │   ├── fixtures.py
    │           │   │   ├── plugin
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── bootstrap.py
    │           │   │   ├── requirements.py
    │           │   │   ├── schemacompare.py
    │           │   │   ├── suite
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _autogen_fixtures.py
    │           │   │   │   ├── test_autogen_comments.py
    │           │   │   │   ├── test_autogen_computed.py
    │           │   │   │   ├── test_autogen_diffs.py
    │           │   │   │   ├── test_autogen_fks.py
    │           │   │   │   ├── test_autogen_identity.py
    │           │   │   │   ├── test_environment.py
    │           │   │   │   └── test_op.py
    │           │   │   ├── util.py
    │           │   │   └── warnings.py
    │           │   └── util
    │           │       ├── __init__.py
    │           │       ├── compat.py
    │           │       ├── editor.py
    │           │       ├── exc.py
    │           │       ├── langhelpers.py
    │           │       ├── messaging.py
    │           │       ├── pyfiles.py
    │           │       └── sqla_compat.py
    │           ├── alembic-1.20.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── amqp
    │           │   ├── __init__.py
    │           │   ├── abstract_channel.py
    │           │   ├── basic_message.py
    │           │   ├── channel.py
    │           │   ├── connection.py
    │           │   ├── exceptions.py
    │           │   ├── method_framing.py
    │           │   ├── platform.py
    │           │   ├── protocol.py
    │           │   ├── sasl.py
    │           │   ├── serialization.py
    │           │   ├── spec.py
    │           │   ├── transport.py
    │           │   └── utils.py
    │           ├── amqp-5.4.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── annotated_doc
    │           │   ├── __init__.py
    │           │   ├── main.py
    │           │   └── py.typed
    │           ├── annotated_doc-0.0.6.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── annotated_types
    │           │   ├── __init__.py
    │           │   ├── py.typed
    │           │   └── test_cases.py
    │           ├── annotated_types-0.8.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── anyio
    │           │   ├── __init__.py
    │           │   ├── _backends
    │           │   │   ├── __init__.py
    │           │   │   ├── _asyncio.py
    │           │   │   └── _trio.py
    │           │   ├── _core
    │           │   │   ├── __init__.py
    │           │   │   ├── _asyncio_selector_thread.py
    │           │   │   ├── _concurrency_utils.py
    │           │   │   ├── _contextmanagers.py
    │           │   │   ├── _eventloop.py
    │           │   │   ├── _exceptions.py
    │           │   │   ├── _fileio.py
    │           │   │   ├── _futures.py
    │           │   │   ├── _resources.py
    │           │   │   ├── _signals.py
    │           │   │   ├── _sockets.py
    │           │   │   ├── _streams.py
    │           │   │   ├── _subprocesses.py
    │           │   │   ├── _synchronization.py
    │           │   │   ├── _tasks.py
    │           │   │   ├── _tempfile.py
    │           │   │   ├── _testing.py
    │           │   │   └── _typedattr.py
    │           │   ├── _lazyimport.py
    │           │   ├── abc
    │           │   │   ├── __init__.py
    │           │   │   ├── _eventloop.py
    │           │   │   ├── _resources.py
    │           │   │   ├── _sockets.py
    │           │   │   ├── _streams.py
    │           │   │   ├── _subprocesses.py
    │           │   │   ├── _tasks.py
    │           │   │   └── _testing.py
    │           │   ├── from_thread.py
    │           │   ├── functools.py
    │           │   ├── itertools.py
    │           │   ├── lowlevel.py
    │           │   ├── py.typed
    │           │   ├── pytest_plugin.py
    │           │   ├── streams
    │           │   │   ├── __init__.py
    │           │   │   ├── buffered.py
    │           │   │   ├── file.py
    │           │   │   ├── memory.py
    │           │   │   ├── stapled.py
    │           │   │   ├── text.py
    │           │   │   └── tls.py
    │           │   ├── to_interpreter.py
    │           │   ├── to_process.py
    │           │   └── to_thread.py
    │           ├── anyio-4.16.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── asyncpg
    │           │   ├── __init__.py
    │           │   ├── _asyncio_compat.py
    │           │   ├── _testbase
    │           │   │   ├── __init__.py
    │           │   │   └── fuzzer.py
    │           │   ├── _version.py
    │           │   ├── cluster.py
    │           │   ├── compat.py
    │           │   ├── connect_utils.py
    │           │   ├── connection.py
    │           │   ├── connresource.py
    │           │   ├── cursor.py
    │           │   ├── exceptions
    │           │   │   ├── __init__.py
    │           │   │   └── _base.py
    │           │   ├── introspection.py
    │           │   ├── pgproto
    │           │   │   ├── __init__.pxd
    │           │   │   ├── __init__.py
    │           │   │   ├── buffer.pxd
    │           │   │   ├── buffer.pxi
    │           │   │   ├── buffer.pyx
    │           │   │   ├── codecs
    │           │   │   │   ├── __init__.pxd
    │           │   │   │   ├── bits.pyx
    │           │   │   │   ├── bytea.pyx
    │           │   │   │   ├── context.pyx
    │           │   │   │   ├── datetime.pyx
    │           │   │   │   ├── float.pyx
    │           │   │   │   ├── geometry.pyx
    │           │   │   │   ├── hstore.pyx
    │           │   │   │   ├── int.pyx
    │           │   │   │   ├── json.pyx
    │           │   │   │   ├── jsonpath.pyx
    │           │   │   │   ├── misc.pyx
    │           │   │   │   ├── network.pyx
    │           │   │   │   ├── numeric.pyx
    │           │   │   │   ├── pg_snapshot.pyx
    │           │   │   │   ├── text.pyx
    │           │   │   │   ├── tid.pyx
    │           │   │   │   └── uuid.pyx
    │           │   │   ├── consts.pxi
    │           │   │   ├── cpythonx.pxd
    │           │   │   ├── debug.pxd
    │           │   │   ├── frb.pxd
    │           │   │   ├── frb.pyx
    │           │   │   ├── hton.pxd
    │           │   │   ├── pgproto.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── pgproto.pxd
    │           │   │   ├── pgproto.pyi
    │           │   │   ├── pgproto.pyx
    │           │   │   ├── tohex.pxd
    │           │   │   ├── types.py
    │           │   │   └── uuid.pyx
    │           │   ├── pool.py
    │           │   ├── prepared_stmt.py
    │           │   ├── protocol
    │           │   │   ├── __init__.py
    │           │   │   ├── codecs
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── array.pyx
    │           │   │   │   ├── base.pxd
    │           │   │   │   ├── base.pyx
    │           │   │   │   ├── pgproto.pyx
    │           │   │   │   ├── range.pyx
    │           │   │   │   ├── record.pyx
    │           │   │   │   └── textutils.pyx
    │           │   │   ├── consts.pxi
    │           │   │   ├── coreproto.pxd
    │           │   │   ├── coreproto.pyx
    │           │   │   ├── cpythonx.pxd
    │           │   │   ├── encodings.pyx
    │           │   │   ├── pgtypes.pxi
    │           │   │   ├── prepared_stmt.pxd
    │           │   │   ├── prepared_stmt.pyx
    │           │   │   ├── protocol.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── protocol.pxd
    │           │   │   ├── protocol.pyi
    │           │   │   ├── protocol.pyx
    │           │   │   ├── record.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── record.pyi
    │           │   │   ├── recordcapi.pxd
    │           │   │   ├── scram.pxd
    │           │   │   ├── scram.pyx
    │           │   │   ├── settings.pxd
    │           │   │   └── settings.pyx
    │           │   ├── serverversion.py
    │           │   ├── transaction.py
    │           │   ├── types.py
    │           │   └── utils.py
    │           ├── asyncpg-0.32.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── billiard
    │           │   ├── __init__.py
    │           │   ├── _ext.py
    │           │   ├── _win.py
    │           │   ├── common.py
    │           │   ├── compat.py
    │           │   ├── connection.py
    │           │   ├── context.py
    │           │   ├── dummy
    │           │   │   ├── __init__.py
    │           │   │   └── connection.py
    │           │   ├── einfo.py
    │           │   ├── exceptions.py
    │           │   ├── forkserver.py
    │           │   ├── heap.py
    │           │   ├── managers.py
    │           │   ├── pool.py
    │           │   ├── popen_fork.py
    │           │   ├── popen_forkserver.py
    │           │   ├── popen_spawn_posix.py
    │           │   ├── popen_spawn_win32.py
    │           │   ├── process.py
    │           │   ├── queues.py
    │           │   ├── reduction.py
    │           │   ├── resource_sharer.py
    │           │   ├── semaphore_tracker.py
    │           │   ├── sharedctypes.py
    │           │   ├── spawn.py
    │           │   ├── synchronize.py
    │           │   └── util.py
    │           ├── billiard-4.3.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── celery
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _state.py
    │           │   ├── app
    │           │   │   ├── __init__.py
    │           │   │   ├── amqp.py
    │           │   │   ├── annotations.py
    │           │   │   ├── autoretry.py
    │           │   │   ├── backends.py
    │           │   │   ├── base.py
    │           │   │   ├── builtins.py
    │           │   │   ├── control.py
    │           │   │   ├── defaults.py
    │           │   │   ├── events.py
    │           │   │   ├── log.py
    │           │   │   ├── registry.py
    │           │   │   ├── routes.py
    │           │   │   ├── task.py
    │           │   │   ├── trace.py
    │           │   │   └── utils.py
    │           │   ├── apps
    │           │   │   ├── __init__.py
    │           │   │   ├── beat.py
    │           │   │   ├── multi.py
    │           │   │   └── worker.py
    │           │   ├── backends
    │           │   │   ├── __init__.py
    │           │   │   ├── arangodb.py
    │           │   │   ├── asynchronous.py
    │           │   │   ├── azureblockblob.py
    │           │   │   ├── base.py
    │           │   │   ├── cache.py
    │           │   │   ├── cassandra.py
    │           │   │   ├── consul.py
    │           │   │   ├── cosmosdbsql.py
    │           │   │   ├── couchbase.py
    │           │   │   ├── couchdb.py
    │           │   │   ├── database
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── models.py
    │           │   │   │   └── session.py
    │           │   │   ├── dynamodb.py
    │           │   │   ├── elasticsearch.py
    │           │   │   ├── filesystem.py
    │           │   │   ├── gcs.py
    │           │   │   ├── mongodb.py
    │           │   │   ├── redis.py
    │           │   │   ├── rpc.py
    │           │   │   └── s3.py
    │           │   ├── beat.py
    │           │   ├── bin
    │           │   │   ├── __init__.py
    │           │   │   ├── amqp.py
    │           │   │   ├── base.py
    │           │   │   ├── beat.py
    │           │   │   ├── call.py
    │           │   │   ├── celery.py
    │           │   │   ├── control.py
    │           │   │   ├── events.py
    │           │   │   ├── graph.py
    │           │   │   ├── list.py
    │           │   │   ├── logtool.py
    │           │   │   ├── migrate.py
    │           │   │   ├── multi.py
    │           │   │   ├── purge.py
    │           │   │   ├── result.py
    │           │   │   ├── shell.py
    │           │   │   ├── upgrade.py
    │           │   │   └── worker.py
    │           │   ├── bootsteps.py
    │           │   ├── canvas.py
    │           │   ├── concurrency
    │           │   │   ├── __init__.py
    │           │   │   ├── asynpool.py
    │           │   │   ├── base.py
    │           │   │   ├── eventlet.py
    │           │   │   ├── gevent.py
    │           │   │   ├── prefork.py
    │           │   │   ├── solo.py
    │           │   │   └── thread.py
    │           │   ├── contrib
    │           │   │   ├── __init__.py
    │           │   │   ├── abortable.py
    │           │   │   ├── django
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── task.py
    │           │   │   ├── migrate.py
    │           │   │   ├── pytest.py
    │           │   │   ├── rdb.py
    │           │   │   ├── sphinx.py
    │           │   │   └── testing
    │           │   │       ├── __init__.py
    │           │   │       ├── app.py
    │           │   │       ├── manager.py
    │           │   │       ├── mocks.py
    │           │   │       ├── tasks.py
    │           │   │       └── worker.py
    │           │   ├── events
    │           │   │   ├── __init__.py
    │           │   │   ├── cursesmon.py
    │           │   │   ├── dispatcher.py
    │           │   │   ├── dumper.py
    │           │   │   ├── event.py
    │           │   │   ├── receiver.py
    │           │   │   ├── snapshot.py
    │           │   │   └── state.py
    │           │   ├── exceptions.py
    │           │   ├── fixups
    │           │   │   ├── __init__.py
    │           │   │   └── django.py
    │           │   ├── loaders
    │           │   │   ├── __init__.py
    │           │   │   ├── app.py
    │           │   │   ├── base.py
    │           │   │   └── default.py
    │           │   ├── local.py
    │           │   ├── platforms.py
    │           │   ├── result.py
    │           │   ├── schedules.py
    │           │   ├── security
    │           │   │   ├── __init__.py
    │           │   │   ├── certificate.py
    │           │   │   ├── key.py
    │           │   │   ├── serialization.py
    │           │   │   └── utils.py
    │           │   ├── signals.py
    │           │   ├── states.py
    │           │   ├── utils
    │           │   │   ├── __init__.py
    │           │   │   ├── abstract.py
    │           │   │   ├── annotations.py
    │           │   │   ├── collections.py
    │           │   │   ├── debug.py
    │           │   │   ├── deprecated.py
    │           │   │   ├── dispatch
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── signal.py
    │           │   │   ├── functional.py
    │           │   │   ├── graph.py
    │           │   │   ├── imports.py
    │           │   │   ├── iso8601.py
    │           │   │   ├── log.py
    │           │   │   ├── nodenames.py
    │           │   │   ├── objects.py
    │           │   │   ├── quorum_queues.py
    │           │   │   ├── saferepr.py
    │           │   │   ├── serialization.py
    │           │   │   ├── static
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── celery_128.png
    │           │   │   ├── sysinfo.py
    │           │   │   ├── term.py
    │           │   │   ├── text.py
    │           │   │   ├── threads.py
    │           │   │   ├── time.py
    │           │   │   └── timer2.py
    │           │   └── worker
    │           │       ├── __init__.py
    │           │       ├── autoscale.py
    │           │       ├── components.py
    │           │       ├── consumer
    │           │       │   ├── __init__.py
    │           │       │   ├── agent.py
    │           │       │   ├── connection.py
    │           │       │   ├── consumer.py
    │           │       │   ├── control.py
    │           │       │   ├── delayed_delivery.py
    │           │       │   ├── events.py
    │           │       │   ├── gossip.py
    │           │       │   ├── heart.py
    │           │       │   ├── mingle.py
    │           │       │   └── tasks.py
    │           │       ├── control.py
    │           │       ├── heartbeat.py
    │           │       ├── loops.py
    │           │       ├── pidbox.py
    │           │       ├── request.py
    │           │       ├── state.py
    │           │       ├── strategy.py
    │           │       └── worker.py
    │           ├── celery-5.7.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── certifi
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── cacert.pem
    │           │   ├── core.py
    │           │   ├── py.typed
    │           │   └── tests
    │           │       ├── __init__.py
    │           │       └── test_certify.py
    │           ├── certifi-2026.10.23.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── charset_normalizer
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── api.py
    │           │   ├── cd.cpython-314-x86_64-linux-gnu.so
    │           │   ├── cd.py
    │           │   ├── cli
    │           │   │   ├── __init__.py
    │           │   │   └── __main__.py
    │           │   ├── constant.py
    │           │   ├── legacy.py
    │           │   ├── md.cpython-314-x86_64-linux-gnu.so
    │           │   ├── md.py
    │           │   ├── models.py
    │           │   ├── py.typed
    │           │   ├── utils.py
    │           │   └── version.py
    │           ├── charset_normalizer-3.5.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── click
    │           │   ├── __init__.py
    │           │   ├── _compat.py
    │           │   ├── _termui_impl.py
    │           │   ├── _textwrap.py
    │           │   ├── _utils.py
    │           │   ├── _winconsole.py
    │           │   ├── core.py
    │           │   ├── decorators.py
    │           │   ├── exceptions.py
    │           │   ├── formatting.py
    │           │   ├── globals.py
    │           │   ├── parser.py
    │           │   ├── py.typed
    │           │   ├── shell_completion.py
    │           │   ├── termui.py
    │           │   ├── testing.py
    │           │   ├── types.py
    │           │   └── utils.py
    │           ├── click-8.5.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE.txt
    │           ├── click_didyoumean
    │           │   └── __init__.py
    │           ├── click_didyoumean-0.3.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   └── WHEEL
    │           ├── click_plugins
    │           │   ├── __init__.py
    │           │   └── core.py
    │           ├── click_plugins-1.1.1.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── AUTHORS.txt
    │           │   │   └── LICENSE.txt
    │           │   ├── top_level.txt
    │           │   └── zip-safe
    │           ├── click_plugins.py
    │           ├── click_repl
    │           │   ├── __init__.py
    │           │   ├── _completer.py
    │           │   ├── _ctx_stack.py
    │           │   ├── _repl.py
    │           │   ├── core.py
    │           │   ├── exceptions.py
    │           │   ├── globals_.py
    │           │   ├── py.typed
    │           │   └── utils.py
    │           ├── click_repl-0.4.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── cv2
    │           │   ├── Error
    │           │   │   └── __init__.pyi
    │           │   ├── LICENSE-3RD-PARTY.txt
    │           │   ├── LICENSE.txt
    │           │   ├── __init__.py
    │           │   ├── __init__.pyi
    │           │   ├── aruco
    │           │   │   └── __init__.pyi
    │           │   ├── barcode
    │           │   │   └── __init__.pyi
    │           │   ├── ccm
    │           │   │   └── __init__.pyi
    │           │   ├── config-3.py
    │           │   ├── config.py
    │           │   ├── cuda
    │           │   │   └── __init__.pyi
    │           │   ├── cv2.abi3.so
    │           │   ├── data
    │           │   │   └── __init__.py
    │           │   ├── detail
    │           │   │   └── __init__.pyi
    │           │   ├── dnn
    │           │   │   └── __init__.pyi
    │           │   ├── fisheye
    │           │   │   └── __init__.pyi
    │           │   ├── flann
    │           │   │   └── __init__.pyi
    │           │   ├── instr
    │           │   │   └── __init__.pyi
    │           │   ├── ipp
    │           │   │   └── __init__.pyi
    │           │   ├── load_config_py2.py
    │           │   ├── load_config_py3.py
    │           │   ├── mat_wrapper
    │           │   │   └── __init__.py
    │           │   ├── mcc
    │           │   │   └── __init__.pyi
    │           │   ├── misc
    │           │   │   ├── __init__.py
    │           │   │   └── version.py
    │           │   ├── ocl
    │           │   │   └── __init__.pyi
    │           │   ├── ogl
    │           │   │   └── __init__.pyi
    │           │   ├── parallel
    │           │   │   └── __init__.pyi
    │           │   ├── py.typed
    │           │   ├── samples
    │           │   │   └── __init__.pyi
    │           │   ├── segmentation
    │           │   │   └── __init__.pyi
    │           │   ├── typing
    │           │   │   └── __init__.py
    │           │   ├── utils
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── fs
    │           │   │   │   └── __init__.pyi
    │           │   │   ├── logging
    │           │   │   │   └── __init__.pyi
    │           │   │   └── nested
    │           │   │       └── __init__.pyi
    │           │   ├── version.py
    │           │   └── videoio_registry
    │           │       └── __init__.pyi
    │           ├── dateutil
    │           │   ├── __init__.py
    │           │   ├── _common.py
    │           │   ├── _version.py
    │           │   ├── easter.py
    │           │   ├── parser
    │           │   │   ├── __init__.py
    │           │   │   ├── _parser.py
    │           │   │   └── isoparser.py
    │           │   ├── relativedelta.py
    │           │   ├── rrule.py
    │           │   ├── tz
    │           │   │   ├── __init__.py
    │           │   │   ├── _common.py
    │           │   │   ├── _factories.py
    │           │   │   ├── tz.py
    │           │   │   └── win.py
    │           │   ├── tzwin.py
    │           │   ├── utils.py
    │           │   └── zoneinfo
    │           │       ├── __init__.py
    │           │       ├── dateutil-zoneinfo.tar.gz
    │           │       └── rebuild.py
    │           ├── distro
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── distro.py
    │           │   └── py.typed
    │           ├── distro-1.9.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── top_level.txt
    │           ├── dotenv
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── cli.py
    │           │   ├── ipython.py
    │           │   ├── main.py
    │           │   ├── parser.py
    │           │   ├── py.typed
    │           │   ├── variables.py
    │           │   └── version.py
    │           ├── et_xmlfile
    │           │   ├── __init__.py
    │           │   ├── incremental_tree.py
    │           │   └── xmlfile.py
    │           ├── et_xmlfile-2.0.0.dist-info
    │           │   ├── AUTHORS.txt
    │           │   ├── INSTALLER
    │           │   ├── LICENCE.python
    │           │   ├── LICENCE.rst
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── fastapi
    │           │   ├── .agents
    │           │   │   └── skills
    │           │   │       └── fastapi
    │           │   │           ├── SKILL.md
    │           │   │           └── references
    │           │   │               ├── dependencies.md
    │           │   │               ├── fastapi-cloud.md
    │           │   │               ├── other-tools.md
    │           │   │               ├── parameter-models.md
    │           │   │               ├── path-operations.md
    │           │   │               ├── pydantic.md
    │           │   │               ├── responses.md
    │           │   │               └── streaming.md
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _compat
    │           │   │   ├── __init__.py
    │           │   │   ├── shared.py
    │           │   │   └── v2.py
    │           │   ├── applications.py
    │           │   ├── background.py
    │           │   ├── cli.py
    │           │   ├── concurrency.py
    │           │   ├── datastructures.py
    │           │   ├── dependencies
    │           │   │   ├── __init__.py
    │           │   │   ├── models.py
    │           │   │   └── utils.py
    │           │   ├── encoders.py
    │           │   ├── exception_handlers.py
    │           │   ├── exceptions.py
    │           │   ├── logger.py
    │           │   ├── middleware
    │           │   │   ├── __init__.py
    │           │   │   ├── asyncexitstack.py
    │           │   │   ├── cors.py
    │           │   │   ├── gzip.py
    │           │   │   ├── httpsredirect.py
    │           │   │   ├── trustedhost.py
    │           │   │   └── wsgi.py
    │           │   ├── openapi
    │           │   │   ├── __init__.py
    │           │   │   ├── constants.py
    │           │   │   ├── docs.py
    │           │   │   ├── models.py
    │           │   │   └── utils.py
    │           │   ├── param_functions.py
    │           │   ├── params.py
    │           │   ├── py.typed
    │           │   ├── requests.py
    │           │   ├── responses.py
    │           │   ├── routing.py
    │           │   ├── security
    │           │   │   ├── __init__.py
    │           │   │   ├── api_key.py
    │           │   │   ├── base.py
    │           │   │   ├── http.py
    │           │   │   ├── oauth2.py
    │           │   │   ├── open_id_connect_url.py
    │           │   │   └── utils.py
    │           │   ├── sse.py
    │           │   ├── staticfiles.py
    │           │   ├── telemetry
    │           │   │   ├── __init__.py
    │           │   │   ├── _api.py
    │           │   │   ├── _asgi.py
    │           │   │   └── _runtime.py
    │           │   ├── templating.py
    │           │   ├── testclient.py
    │           │   ├── types.py
    │           │   ├── utils.py
    │           │   └── websockets.py
    │           ├── fastapi-0.163.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── fastembed
    │           │   ├── __init__.py
    │           │   ├── common
    │           │   │   ├── __init__.py
    │           │   │   ├── model_description.py
    │           │   │   ├── model_management.py
    │           │   │   ├── onnx_external_data.py
    │           │   │   ├── onnx_model.py
    │           │   │   ├── preprocessor_utils.py
    │           │   │   ├── safetensors_utils.py
    │           │   │   ├── types.py
    │           │   │   └── utils.py
    │           │   ├── embedding.py
    │           │   ├── image
    │           │   │   ├── __init__.py
    │           │   │   ├── image_embedding.py
    │           │   │   ├── image_embedding_base.py
    │           │   │   ├── normalized_embedding.py
    │           │   │   ├── onnx_embedding.py
    │           │   │   ├── onnx_image_model.py
    │           │   │   ├── siglip_embedding.py
    │           │   │   └── transform
    │           │   │       ├── functional.py
    │           │   │       └── operators.py
    │           │   ├── late_interaction
    │           │   │   ├── __init__.py
    │           │   │   ├── colbert.py
    │           │   │   ├── jina_colbert.py
    │           │   │   ├── late_interaction_embedding_base.py
    │           │   │   ├── late_interaction_text_embedding.py
    │           │   │   ├── lateon.py
    │           │   │   └── token_embeddings.py
    │           │   ├── late_interaction_multimodal
    │           │   │   ├── __init__.py
    │           │   │   ├── colmodernvbert.py
    │           │   │   ├── colpali.py
    │           │   │   ├── late_interaction_multimodal_embedding.py
    │           │   │   ├── late_interaction_multimodal_embedding_base.py
    │           │   │   └── onnx_multimodal_model.py
    │           │   ├── parallel_processor.py
    │           │   ├── postprocess
    │           │   │   ├── __init__.py
    │           │   │   └── muvera.py
    │           │   ├── py.typed
    │           │   ├── rerank
    │           │   │   └── cross_encoder
    │           │   │       ├── __init__.py
    │           │   │       ├── custom_text_cross_encoder.py
    │           │   │       ├── onnx_text_cross_encoder.py
    │           │   │       ├── onnx_text_model.py
    │           │   │       ├── text_cross_encoder.py
    │           │   │       └── text_cross_encoder_base.py
    │           │   ├── sparse
    │           │   │   ├── __init__.py
    │           │   │   ├── bm25.py
    │           │   │   ├── bm42.py
    │           │   │   ├── if_splade.py
    │           │   │   ├── minicoil.py
    │           │   │   ├── sparse_embedding_base.py
    │           │   │   ├── sparse_text_embedding.py
    │           │   │   ├── splade_pp.py
    │           │   │   └── utils
    │           │   │       ├── minicoil_encoder.py
    │           │   │       ├── sparse_vectors_converter.py
    │           │   │       ├── tokenizer.py
    │           │   │       └── vocab_resolver.py
    │           │   └── text
    │           │       ├── __init__.py
    │           │       ├── builtin_sentence_embedding.py
    │           │       ├── clip_embedding.py
    │           │       ├── custom_text_embedding.py
    │           │       ├── last_token_normalized_embedding.py
    │           │       ├── multitask_embedding.py
    │           │       ├── onnx_embedding.py
    │           │       ├── onnx_text_model.py
    │           │       ├── pooled_embedding.py
    │           │       ├── pooled_normalized_embedding.py
    │           │       ├── siglip_embedding.py
    │           │       ├── static_embedding.py
    │           │       ├── text_embedding.py
    │           │       └── text_embedding_base.py
    │           ├── fastembed-0.9.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       ├── LICENSE
    │           │       └── NOTICE
    │           ├── filelock
    │           │   ├── __init__.py
    │           │   ├── _api.py
    │           │   ├── _async.py
    │           │   ├── _async_read_write.py
    │           │   ├── _descriptor.py
    │           │   ├── _error.py
    │           │   ├── _identity.py
    │           │   ├── _lease.py
    │           │   ├── _marker.py
    │           │   ├── _read_write.py
    │           │   ├── _soft.py
    │           │   ├── _soft_protocol.py
    │           │   ├── _soft_rw
    │           │   │   ├── __init__.py
    │           │   │   ├── _async.py
    │           │   │   ├── _protocol.py
    │           │   │   ├── _storage.py
    │           │   │   └── _sync.py
    │           │   ├── _strict.py
    │           │   ├── _unix.py
    │           │   ├── _util.py
    │           │   ├── _windows.py
    │           │   ├── asyncio.py
    │           │   ├── py.typed
    │           │   └── version.py
    │           ├── filelock-4.2.10.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── sboms
    │           │       └── filelock.cdx.json
    │           ├── fitz
    │           │   ├── __init__.py
    │           │   ├── table.py
    │           │   └── utils.py
    │           ├── flatbuffers
    │           │   ├── __init__.py
    │           │   ├── _version.py
    │           │   ├── builder.py
    │           │   ├── compat.py
    │           │   ├── encode.py
    │           │   ├── flexbuffers.py
    │           │   ├── number_types.py
    │           │   ├── packer.py
    │           │   ├── table.py
    │           │   └── util.py
    │           ├── flatbuffers-25.12.19.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── fsspec
    │           │   ├── __init__.py
    │           │   ├── _version.py
    │           │   ├── archive.py
    │           │   ├── asyn.py
    │           │   ├── caching.py
    │           │   ├── callbacks.py
    │           │   ├── compression.py
    │           │   ├── config.py
    │           │   ├── conftest.py
    │           │   ├── core.py
    │           │   ├── dircache.py
    │           │   ├── exceptions.py
    │           │   ├── fuse.py
    │           │   ├── generic.py
    │           │   ├── gui.py
    │           │   ├── implementations
    │           │   │   ├── __init__.py
    │           │   │   ├── arrow.py
    │           │   │   ├── asyn_wrapper.py
    │           │   │   ├── cache_mapper.py
    │           │   │   ├── cache_metadata.py
    │           │   │   ├── cached.py
    │           │   │   ├── chained.py
    │           │   │   ├── dask.py
    │           │   │   ├── data.py
    │           │   │   ├── dbfs.py
    │           │   │   ├── dirfs.py
    │           │   │   ├── ftp.py
    │           │   │   ├── gist.py
    │           │   │   ├── git.py
    │           │   │   ├── github.py
    │           │   │   ├── http.py
    │           │   │   ├── http_sync.py
    │           │   │   ├── jupyter.py
    │           │   │   ├── libarchive.py
    │           │   │   ├── local.py
    │           │   │   ├── memory.py
    │           │   │   ├── reference.py
    │           │   │   ├── sftp.py
    │           │   │   ├── smb.py
    │           │   │   ├── tar.py
    │           │   │   ├── webhdfs.py
    │           │   │   └── zip.py
    │           │   ├── json.py
    │           │   ├── mapping.py
    │           │   ├── parquet.py
    │           │   ├── prefetcher.py
    │           │   ├── registry.py
    │           │   ├── spec.py
    │           │   ├── tests
    │           │   │   └── abstract
    │           │   │       ├── __init__.py
    │           │   │       ├── common.py
    │           │   │       ├── copy.py
    │           │   │       ├── get.py
    │           │   │       ├── mv.py
    │           │   │       ├── open.py
    │           │   │       ├── pipe.py
    │           │   │       └── put.py
    │           │   ├── transaction.py
    │           │   └── utils.py
    │           ├── fsspec-2026.9.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── google
    │           │   ├── _upb
    │           │   │   └── _message.abi3.so
    │           │   └── protobuf
    │           │       ├── __init__.py
    │           │       ├── any.py
    │           │       ├── any_pb2.py
    │           │       ├── api_pb2.py
    │           │       ├── compiler
    │           │       │   ├── __init__.py
    │           │       │   └── plugin_pb2.py
    │           │       ├── descriptor.py
    │           │       ├── descriptor_database.py
    │           │       ├── descriptor_pb2.py
    │           │       ├── descriptor_pool.py
    │           │       ├── duration.py
    │           │       ├── duration_pb2.py
    │           │       ├── empty_pb2.py
    │           │       ├── field_mask_pb2.py
    │           │       ├── internal
    │           │       │   ├── __init__.py
    │           │       │   ├── api_implementation.py
    │           │       │   ├── builder.py
    │           │       │   ├── containers.py
    │           │       │   ├── decoder.py
    │           │       │   ├── encoder.py
    │           │       │   ├── enum_type_wrapper.py
    │           │       │   ├── extension_dict.py
    │           │       │   ├── field_mask.py
    │           │       │   ├── json_format_benchmark.py
    │           │       │   ├── message_benchmark.py
    │           │       │   ├── message_listener.py
    │           │       │   ├── python_edition_defaults.py
    │           │       │   ├── python_message.py
    │           │       │   ├── testing_refleaks.py
    │           │       │   ├── type_checkers.py
    │           │       │   ├── well_known_types.py
    │           │       │   └── wire_format.py
    │           │       ├── json_enumvalue_options_pb2.py
    │           │       ├── json_format.py
    │           │       ├── json_options_pb2.py
    │           │       ├── message.py
    │           │       ├── message_factory.py
    │           │       ├── proto.py
    │           │       ├── proto_builder.py
    │           │       ├── proto_json.py
    │           │       ├── proto_text.py
    │           │       ├── pyext
    │           │       │   ├── __init__.py
    │           │       │   └── cpp_message.py
    │           │       ├── reflection.py
    │           │       ├── runtime_version.py
    │           │       ├── service_reflection.py
    │           │       ├── source_context_pb2.py
    │           │       ├── struct_pb2.py
    │           │       ├── symbol_database.py
    │           │       ├── testdata
    │           │       │   └── __init__.py
    │           │       ├── text_encoding.py
    │           │       ├── text_format.py
    │           │       ├── timestamp.py
    │           │       ├── timestamp_pb2.py
    │           │       ├── type_pb2.py
    │           │       ├── unknown_fields.py
    │           │       ├── util
    │           │       │   └── __init__.py
    │           │       └── wrappers_pb2.py
    │           ├── greenlet
    │           │   ├── CObjects.cpp
    │           │   ├── PyGreenlet.cpp
    │           │   ├── PyGreenlet.hpp
    │           │   ├── PyGreenletUnswitchable.cpp
    │           │   ├── PyModule.cpp
    │           │   ├── TBrokenGreenlet.cpp
    │           │   ├── TExceptionState.cpp
    │           │   ├── TGreenlet.cpp
    │           │   ├── TGreenlet.hpp
    │           │   ├── TGreenletGlobals.cpp
    │           │   ├── TMainGreenlet.cpp
    │           │   ├── TPythonState.cpp
    │           │   ├── TStackState.cpp
    │           │   ├── TThreadState.hpp
    │           │   ├── TThreadStateCreator.hpp
    │           │   ├── TThreadStateDestroy.cpp
    │           │   ├── TUserGreenlet.cpp
    │           │   ├── __init__.py
    │           │   ├── _greenlet.cpython-314-x86_64-linux-gnu.so
    │           │   ├── greenlet.cpp
    │           │   ├── greenlet.h
    │           │   ├── greenlet_allocator.hpp
    │           │   ├── greenlet_compiler_compat.hpp
    │           │   ├── greenlet_cpython_compat.hpp
    │           │   ├── greenlet_exceptions.hpp
    │           │   ├── greenlet_internal.hpp
    │           │   ├── greenlet_msvc_compat.hpp
    │           │   ├── greenlet_refs.hpp
    │           │   ├── greenlet_slp_switch.hpp
    │           │   ├── greenlet_thread_support.hpp
    │           │   ├── platform
    │           │   │   ├── __init__.py
    │           │   │   ├── setup_switch_x64_masm.cmd
    │           │   │   ├── switch_aarch64_gcc.h
    │           │   │   ├── switch_alpha_unix.h
    │           │   │   ├── switch_amd64_unix.h
    │           │   │   ├── switch_arm32_gcc.h
    │           │   │   ├── switch_arm32_ios.h
    │           │   │   ├── switch_arm64_masm.asm
    │           │   │   ├── switch_arm64_masm.obj
    │           │   │   ├── switch_arm64_msvc.h
    │           │   │   ├── switch_csky_gcc.h
    │           │   │   ├── switch_loongarch64_linux.h
    │           │   │   ├── switch_m68k_gcc.h
    │           │   │   ├── switch_mips_unix.h
    │           │   │   ├── switch_ppc64_aix.h
    │           │   │   ├── switch_ppc64_linux.h
    │           │   │   ├── switch_ppc_aix.h
    │           │   │   ├── switch_ppc_linux.h
    │           │   │   ├── switch_ppc_macosx.h
    │           │   │   ├── switch_ppc_unix.h
    │           │   │   ├── switch_riscv_unix.h
    │           │   │   ├── switch_s390_unix.h
    │           │   │   ├── switch_sh_gcc.h
    │           │   │   ├── switch_sparc_sun_gcc.h
    │           │   │   ├── switch_x32_unix.h
    │           │   │   ├── switch_x64_masm.asm
    │           │   │   ├── switch_x64_masm.obj
    │           │   │   ├── switch_x64_msvc.h
    │           │   │   ├── switch_x86_msvc.h
    │           │   │   └── switch_x86_unix.h
    │           │   ├── slp_platformselect.h
    │           │   └── tests
    │           │       ├── __init__.py
    │           │       ├── _test_extension.c
    │           │       ├── _test_extension.cpython-314-x86_64-linux-gnu.so
    │           │       ├── _test_extension_cpp.cpp
    │           │       ├── _test_extension_cpp.cpython-314-x86_64-linux-gnu.so
    │           │       ├── fail_c_stack_refs_suspended_gc.py
    │           │       ├── fail_clearing_run_switches.py
    │           │       ├── fail_cpp_exception.py
    │           │       ├── fail_initialstub_already_started.py
    │           │       ├── fail_issue_515_freethread_gc.py
    │           │       ├── fail_slp_switch.py
    │           │       ├── fail_switch_critical_section.py
    │           │       ├── fail_switch_three_greenlets.py
    │           │       ├── fail_switch_three_greenlets2.py
    │           │       ├── fail_switch_two_greenlets.py
    │           │       ├── leakcheck.py
    │           │       ├── test_contextvars.py
    │           │       ├── test_cpp.py
    │           │       ├── test_extension_interface.py
    │           │       ├── test_gc.py
    │           │       ├── test_generator.py
    │           │       ├── test_generator_nested.py
    │           │       ├── test_greenlet.py
    │           │       ├── test_greenlet_trash.py
    │           │       ├── test_interpreter_shutdown.py
    │           │       ├── test_leaks.py
    │           │       ├── test_stack_saved.py
    │           │       ├── test_throw.py
    │           │       ├── test_tracing.py
    │           │       ├── test_version.py
    │           │       └── test_weakref.py
    │           ├── greenlet-3.5.6.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── LICENSE
    │           │   │   └── LICENSE.PSF
    │           │   └── top_level.txt
    │           ├── groq
    │           │   ├── __init__.py
    │           │   ├── _base_client.py
    │           │   ├── _client.py
    │           │   ├── _compat.py
    │           │   ├── _constants.py
    │           │   ├── _exceptions.py
    │           │   ├── _files.py
    │           │   ├── _models.py
    │           │   ├── _qs.py
    │           │   ├── _resource.py
    │           │   ├── _response.py
    │           │   ├── _streaming.py
    │           │   ├── _types.py
    │           │   ├── _utils
    │           │   │   ├── __init__.py
    │           │   │   ├── _compat.py
    │           │   │   ├── _datetime_parse.py
    │           │   │   ├── _json.py
    │           │   │   ├── _logs.py
    │           │   │   ├── _path.py
    │           │   │   ├── _proxy.py
    │           │   │   ├── _reflection.py
    │           │   │   ├── _resources_proxy.py
    │           │   │   ├── _streams.py
    │           │   │   ├── _sync.py
    │           │   │   ├── _transform.py
    │           │   │   ├── _typing.py
    │           │   │   └── _utils.py
    │           │   ├── _version.py
    │           │   ├── lib
    │           │   │   └── .keep
    │           │   ├── py.typed
    │           │   ├── resources
    │           │   │   ├── __init__.py
    │           │   │   ├── audio
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── audio.py
    │           │   │   │   ├── speech.py
    │           │   │   │   ├── transcriptions.py
    │           │   │   │   └── translations.py
    │           │   │   ├── batches.py
    │           │   │   ├── chat
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── chat.py
    │           │   │   │   └── completions.py
    │           │   │   ├── embeddings.py
    │           │   │   ├── files.py
    │           │   │   └── models.py
    │           │   └── types
    │           │       ├── __init__.py
    │           │       ├── audio
    │           │       │   ├── __init__.py
    │           │       │   ├── speech_create_params.py
    │           │       │   ├── transcription.py
    │           │       │   ├── transcription_create_params.py
    │           │       │   ├── translation.py
    │           │       │   └── translation_create_params.py
    │           │       ├── batch_cancel_response.py
    │           │       ├── batch_create_params.py
    │           │       ├── batch_create_response.py
    │           │       ├── batch_list_response.py
    │           │       ├── batch_retrieve_response.py
    │           │       ├── chat
    │           │       │   ├── __init__.py
    │           │       │   ├── chat_completion.py
    │           │       │   ├── chat_completion_assistant_message_param.py
    │           │       │   ├── chat_completion_chunk.py
    │           │       │   ├── chat_completion_content_part_image_param.py
    │           │       │   ├── chat_completion_content_part_param.py
    │           │       │   ├── chat_completion_content_part_text_param.py
    │           │       │   ├── chat_completion_function_call_option_param.py
    │           │       │   ├── chat_completion_function_message_param.py
    │           │       │   ├── chat_completion_message.py
    │           │       │   ├── chat_completion_message_param.py
    │           │       │   ├── chat_completion_message_tool_call.py
    │           │       │   ├── chat_completion_message_tool_call_param.py
    │           │       │   ├── chat_completion_named_tool_choice_param.py
    │           │       │   ├── chat_completion_role.py
    │           │       │   ├── chat_completion_system_message_param.py
    │           │       │   ├── chat_completion_token_logprob.py
    │           │       │   ├── chat_completion_tool_choice_option_param.py
    │           │       │   ├── chat_completion_tool_message_param.py
    │           │       │   ├── chat_completion_tool_param.py
    │           │       │   ├── chat_completion_user_message_param.py
    │           │       │   └── completion_create_params.py
    │           │       ├── completion_usage.py
    │           │       ├── create_embedding_response.py
    │           │       ├── embedding.py
    │           │       ├── embedding_create_params.py
    │           │       ├── file_create_params.py
    │           │       ├── file_create_response.py
    │           │       ├── file_delete_response.py
    │           │       ├── file_info_response.py
    │           │       ├── file_list_response.py
    │           │       ├── model.py
    │           │       ├── model_deleted.py
    │           │       ├── model_list_response.py
    │           │       ├── shared
    │           │       │   ├── __init__.py
    │           │       │   ├── error_object.py
    │           │       │   ├── function_definition.py
    │           │       │   └── function_parameters.py
    │           │       └── shared_params
    │           │           ├── __init__.py
    │           │           ├── function_definition.py
    │           │           └── function_parameters.py
    │           ├── groq-1.7.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── h11
    │           │   ├── __init__.py
    │           │   ├── _abnf.py
    │           │   ├── _connection.py
    │           │   ├── _events.py
    │           │   ├── _headers.py
    │           │   ├── _readers.py
    │           │   ├── _receivebuffer.py
    │           │   ├── _state.py
    │           │   ├── _util.py
    │           │   ├── _version.py
    │           │   ├── _writers.py
    │           │   └── py.typed
    │           ├── h11-0.16.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── hf_xet
    │           │   ├── __init__.py
    │           │   └── hf_xet.abi3.so
    │           ├── hf_xet-1.8.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── sboms
    │           │       └── hf_xet.cyclonedx.json
    │           ├── httpcore
    │           │   ├── __init__.py
    │           │   ├── _api.py
    │           │   ├── _async
    │           │   │   ├── __init__.py
    │           │   │   ├── connection.py
    │           │   │   ├── connection_pool.py
    │           │   │   ├── http11.py
    │           │   │   ├── http2.py
    │           │   │   ├── http_proxy.py
    │           │   │   ├── interfaces.py
    │           │   │   └── socks_proxy.py
    │           │   ├── _backends
    │           │   │   ├── __init__.py
    │           │   │   ├── anyio.py
    │           │   │   ├── auto.py
    │           │   │   ├── base.py
    │           │   │   ├── mock.py
    │           │   │   ├── sync.py
    │           │   │   └── trio.py
    │           │   ├── _exceptions.py
    │           │   ├── _models.py
    │           │   ├── _ssl.py
    │           │   ├── _sync
    │           │   │   ├── __init__.py
    │           │   │   ├── connection.py
    │           │   │   ├── connection_pool.py
    │           │   │   ├── http11.py
    │           │   │   ├── http2.py
    │           │   │   ├── http_proxy.py
    │           │   │   ├── interfaces.py
    │           │   │   └── socks_proxy.py
    │           │   ├── _synchronization.py
    │           │   ├── _trace.py
    │           │   ├── _utils.py
    │           │   └── py.typed
    │           ├── httpcore-1.0.9.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── httpcore2
    │           │   ├── __init__.py
    │           │   ├── _api.py
    │           │   ├── _async
    │           │   │   ├── __init__.py
    │           │   │   ├── connection.py
    │           │   │   ├── connection_pool.py
    │           │   │   ├── http11.py
    │           │   │   ├── http2.py
    │           │   │   ├── http_proxy.py
    │           │   │   ├── interfaces.py
    │           │   │   └── socks_proxy.py
    │           │   ├── _backends
    │           │   │   ├── __init__.py
    │           │   │   ├── anyio.py
    │           │   │   ├── auto.py
    │           │   │   ├── base.py
    │           │   │   ├── mock.py
    │           │   │   ├── sync.py
    │           │   │   └── trio.py
    │           │   ├── _exceptions.py
    │           │   ├── _models.py
    │           │   ├── _ssl.py
    │           │   ├── _sync
    │           │   │   ├── __init__.py
    │           │   │   ├── connection.py
    │           │   │   ├── connection_pool.py
    │           │   │   ├── http11.py
    │           │   │   ├── http2.py
    │           │   │   ├── http_proxy.py
    │           │   │   ├── interfaces.py
    │           │   │   └── socks_proxy.py
    │           │   ├── _synchronization.py
    │           │   ├── _trace.py
    │           │   ├── _utils.py
    │           │   └── py.typed
    │           ├── httpcore2-2.16.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── httptools
    │           │   ├── __init__.py
    │           │   ├── _version.py
    │           │   ├── parser
    │           │   │   ├── __init__.py
    │           │   │   ├── cparser.pxd
    │           │   │   ├── errors.py
    │           │   │   ├── parser.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── parser.pyi
    │           │   │   ├── parser.pyx
    │           │   │   ├── protocol.py
    │           │   │   ├── python.pxd
    │           │   │   ├── url_cparser.pxd
    │           │   │   ├── url_parser.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── url_parser.pyi
    │           │   │   └── url_parser.pyx
    │           │   └── py.typed
    │           ├── httptools-0.9.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── LICENSE
    │           │   │   └── vendor
    │           │   │       ├── http-parser
    │           │   │       │   └── LICENSE-MIT
    │           │   │       └── llhttp
    │           │   │           └── LICENSE
    │           │   └── top_level.txt
    │           ├── httpx
    │           │   ├── __init__.py
    │           │   ├── __version__.py
    │           │   ├── _api.py
    │           │   ├── _auth.py
    │           │   ├── _client.py
    │           │   ├── _config.py
    │           │   ├── _content.py
    │           │   ├── _decoders.py
    │           │   ├── _exceptions.py
    │           │   ├── _main.py
    │           │   ├── _models.py
    │           │   ├── _multipart.py
    │           │   ├── _status_codes.py
    │           │   ├── _transports
    │           │   │   ├── __init__.py
    │           │   │   ├── asgi.py
    │           │   │   ├── base.py
    │           │   │   ├── default.py
    │           │   │   ├── mock.py
    │           │   │   └── wsgi.py
    │           │   ├── _types.py
    │           │   ├── _urlparse.py
    │           │   ├── _urls.py
    │           │   ├── _utils.py
    │           │   └── py.typed
    │           ├── httpx-0.28.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── httpx2
    │           │   ├── __init__.py
    │           │   ├── __version__.py
    │           │   ├── _alias.py
    │           │   ├── _api.py
    │           │   ├── _auth.py
    │           │   ├── _client.py
    │           │   ├── _config.py
    │           │   ├── _content.py
    │           │   ├── _cookies.py
    │           │   ├── _decoders.py
    │           │   ├── _exceptions.py
    │           │   ├── _main.py
    │           │   ├── _models.py
    │           │   ├── _multipart.py
    │           │   ├── _sse.py
    │           │   ├── _status_codes.py
    │           │   ├── _transports
    │           │   │   ├── __init__.py
    │           │   │   ├── asgi.py
    │           │   │   ├── base.py
    │           │   │   ├── default.py
    │           │   │   ├── mock.py
    │           │   │   └── wsgi.py
    │           │   ├── _types.py
    │           │   ├── _urlparse.py
    │           │   ├── _urls.py
    │           │   ├── _utils.py
    │           │   ├── py.typed
    │           │   └── websockets
    │           │       ├── __init__.py
    │           │       ├── _api.py
    │           │       ├── _exceptions.py
    │           │       ├── _ping.py
    │           │       └── _transport.py
    │           ├── httpx2-2.16.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── huggingface_hub
    │           │   ├── __init__.py
    │           │   ├── _buckets.py
    │           │   ├── _commit_api.py
    │           │   ├── _commit_scheduler.py
    │           │   ├── _dataset_viewer.py
    │           │   ├── _eval_results.py
    │           │   ├── _hot_reload
    │           │   │   ├── __init__.py
    │           │   │   ├── client.py
    │           │   │   ├── sse_client.py
    │           │   │   └── types.py
    │           │   ├── _inference_endpoints.py
    │           │   ├── _jobs_api.py
    │           │   ├── _local_folder.py
    │           │   ├── _login.py
    │           │   ├── _oauth.py
    │           │   ├── _oidc.py
    │           │   ├── _revision.py
    │           │   ├── _sandbox.py
    │           │   ├── _sandbox_cache.py
    │           │   ├── _snapshot_download.py
    │           │   ├── _space_api.py
    │           │   ├── _tensorboard_logger.py
    │           │   ├── _tree_cache.py
    │           │   ├── _upload_large_folder.py
    │           │   ├── _upload_pipeline.py
    │           │   ├── _webhooks_payload.py
    │           │   ├── _webhooks_server.py
    │           │   ├── cli
    │           │   │   ├── __init__.py
    │           │   │   ├── _city_game.py
    │           │   │   ├── _cli_utils.py
    │           │   │   ├── _completion.py
    │           │   │   ├── _cp.py
    │           │   │   ├── _errors.py
    │           │   │   ├── _file_listing.py
    │           │   │   ├── _framework.py
    │           │   │   ├── _help_formatter.py
    │           │   │   ├── _output.py
    │           │   │   ├── _skills.py
    │           │   │   ├── _uv_script_header.py
    │           │   │   ├── auth.py
    │           │   │   ├── buckets.py
    │           │   │   ├── cache.py
    │           │   │   ├── collections.py
    │           │   │   ├── datasets.py
    │           │   │   ├── deprecated_cli.py
    │           │   │   ├── discussions.py
    │           │   │   ├── download.py
    │           │   │   ├── extensions.py
    │           │   │   ├── hf.py
    │           │   │   ├── inference_endpoints.py
    │           │   │   ├── jobs.py
    │           │   │   ├── lfs.py
    │           │   │   ├── models.py
    │           │   │   ├── papers.py
    │           │   │   ├── repo_files.py
    │           │   │   ├── repos.py
    │           │   │   ├── sandbox.py
    │           │   │   ├── skills.py
    │           │   │   ├── spaces.py
    │           │   │   ├── system.py
    │           │   │   ├── upload.py
    │           │   │   ├── upload_large_folder.py
    │           │   │   └── webhooks.py
    │           │   ├── community.py
    │           │   ├── constants.py
    │           │   ├── dataclasses.py
    │           │   ├── errors.py
    │           │   ├── fastai_utils.py
    │           │   ├── file_download.py
    │           │   ├── hf_api.py
    │           │   ├── hf_file_system.py
    │           │   ├── hub_mixin.py
    │           │   ├── inference
    │           │   │   ├── __init__.py
    │           │   │   ├── _client.py
    │           │   │   ├── _common.py
    │           │   │   ├── _generated
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _async_client.py
    │           │   │   │   └── types
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── audio_classification.py
    │           │   │   │       ├── audio_to_audio.py
    │           │   │   │       ├── automatic_speech_recognition.py
    │           │   │   │       ├── base.py
    │           │   │   │       ├── chat_completion.py
    │           │   │   │       ├── depth_estimation.py
    │           │   │   │       ├── document_question_answering.py
    │           │   │   │       ├── feature_extraction.py
    │           │   │   │       ├── fill_mask.py
    │           │   │   │       ├── image_classification.py
    │           │   │   │       ├── image_segmentation.py
    │           │   │   │       ├── image_text_to_image.py
    │           │   │   │       ├── image_text_to_video.py
    │           │   │   │       ├── image_to_image.py
    │           │   │   │       ├── image_to_text.py
    │           │   │   │       ├── image_to_video.py
    │           │   │   │       ├── object_detection.py
    │           │   │   │       ├── question_answering.py
    │           │   │   │       ├── sentence_similarity.py
    │           │   │   │       ├── summarization.py
    │           │   │   │       ├── table_question_answering.py
    │           │   │   │       ├── text2text_generation.py
    │           │   │   │       ├── text_classification.py
    │           │   │   │       ├── text_generation.py
    │           │   │   │       ├── text_to_audio.py
    │           │   │   │       ├── text_to_image.py
    │           │   │   │       ├── text_to_speech.py
    │           │   │   │       ├── text_to_video.py
    │           │   │   │       ├── token_classification.py
    │           │   │   │       ├── translation.py
    │           │   │   │       ├── video_classification.py
    │           │   │   │       ├── visual_question_answering.py
    │           │   │   │       ├── zero_shot_classification.py
    │           │   │   │       ├── zero_shot_image_classification.py
    │           │   │   │       └── zero_shot_object_detection.py
    │           │   │   ├── _mcp
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _cli_hacks.py
    │           │   │   │   ├── agent.py
    │           │   │   │   ├── cli.py
    │           │   │   │   ├── constants.py
    │           │   │   │   ├── mcp_client.py
    │           │   │   │   ├── types.py
    │           │   │   │   └── utils.py
    │           │   │   └── _providers
    │           │   │       ├── __init__.py
    │           │   │       ├── _common.py
    │           │   │       ├── baseten.py
    │           │   │       ├── cerebras.py
    │           │   │       ├── cohere.py
    │           │   │       ├── deepinfra.py
    │           │   │       ├── fal_ai.py
    │           │   │       ├── featherless_ai.py
    │           │   │       ├── fireworks_ai.py
    │           │   │       ├── groq.py
    │           │   │       ├── hf_inference.py
    │           │   │       ├── novita.py
    │           │   │       ├── nscale.py
    │           │   │       ├── openai.py
    │           │   │       ├── ovhcloud.py
    │           │   │       ├── publicai.py
    │           │   │       ├── replicate.py
    │           │   │       ├── scaleway.py
    │           │   │       ├── together.py
    │           │   │       ├── wavespeed.py
    │           │   │       └── zai_org.py
    │           │   ├── lfs.py
    │           │   ├── py.typed
    │           │   ├── repocard.py
    │           │   ├── repocard_data.py
    │           │   ├── serialization
    │           │   │   ├── __init__.py
    │           │   │   ├── _base.py
    │           │   │   ├── _dduf.py
    │           │   │   └── _torch.py
    │           │   ├── templates
    │           │   │   ├── datasetcard_template.md
    │           │   │   └── modelcard_template.md
    │           │   └── utils
    │           │       ├── __init__.py
    │           │       ├── _auth.py
    │           │       ├── _cache_assets.py
    │           │       ├── _cache_manager.py
    │           │       ├── _chunk_utils.py
    │           │       ├── _datetime.py
    │           │       ├── _deprecation.py
    │           │       ├── _detect_agent.py
    │           │       ├── _dotenv.py
    │           │       ├── _experimental.py
    │           │       ├── _fixes.py
    │           │       ├── _git_credential.py
    │           │       ├── _headers.py
    │           │       ├── _hf_uris.py
    │           │       ├── _http.py
    │           │       ├── _lfs.py
    │           │       ├── _oauth_device.py
    │           │       ├── _pagination.py
    │           │       ├── _parsing.py
    │           │       ├── _paths.py
    │           │       ├── _runtime.py
    │           │       ├── _safetensors.py
    │           │       ├── _shared_blobs.py
    │           │       ├── _subprocess.py
    │           │       ├── _telemetry.py
    │           │       ├── _terminal.py
    │           │       ├── _typing.py
    │           │       ├── _validators.py
    │           │       ├── _verification.py
    │           │       ├── _xet.py
    │           │       ├── _xet_progress_reporting.py
    │           │       ├── endpoint_helpers.py
    │           │       ├── insecure_hashlib.py
    │           │       ├── logging.py
    │           │       ├── sha.py
    │           │       └── tqdm.py
    │           ├── huggingface_hub-1.33.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── idna
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── cli.py
    │           │   ├── codec.py
    │           │   ├── compat.py
    │           │   ├── core.py
    │           │   ├── idnadata.py
    │           │   ├── intranges.py
    │           │   ├── package_data.py
    │           │   ├── py.typed
    │           │   └── uts46data.py
    │           ├── idna-3.20.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── iniconfig
    │           │   ├── __init__.py
    │           │   ├── _parse.py
    │           │   ├── _version.py
    │           │   ├── exceptions.py
    │           │   └── py.typed
    │           ├── iniconfig-2.3.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── jiter
    │           │   ├── __init__.py
    │           │   ├── __init__.pyi
    │           │   ├── jiter.cpython-314-x86_64-linux-gnu.so
    │           │   └── py.typed
    │           ├── jiter-0.19.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── sboms
    │           │       └── jiter-python.cyclonedx.json
    │           ├── kombu
    │           │   ├── __init__.py
    │           │   ├── abstract.py
    │           │   ├── asynchronous
    │           │   │   ├── __init__.py
    │           │   │   ├── aws
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── connection.py
    │           │   │   │   ├── ext.py
    │           │   │   │   └── sqs
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── connection.py
    │           │   │   │       ├── ext.py
    │           │   │   │       ├── message.py
    │           │   │   │       └── queue.py
    │           │   │   ├── debug.py
    │           │   │   ├── http
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   └── curl.py
    │           │   │   ├── hub.py
    │           │   │   ├── semaphore.py
    │           │   │   └── timer.py
    │           │   ├── clocks.py
    │           │   ├── common.py
    │           │   ├── compat.py
    │           │   ├── compression.py
    │           │   ├── connection.py
    │           │   ├── entity.py
    │           │   ├── exceptions.py
    │           │   ├── log.py
    │           │   ├── matcher.py
    │           │   ├── message.py
    │           │   ├── messaging.py
    │           │   ├── mixins.py
    │           │   ├── pidbox.py
    │           │   ├── pools.py
    │           │   ├── py.typed
    │           │   ├── resource.py
    │           │   ├── serialization.py
    │           │   ├── simple.py
    │           │   ├── transport
    │           │   │   ├── SLMQ.py
    │           │   │   ├── SQS
    │           │   │   │   ├── SNS.py
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── exceptions.py
    │           │   │   ├── __init__.py
    │           │   │   ├── azureservicebus.py
    │           │   │   ├── azurestoragequeues.py
    │           │   │   ├── base.py
    │           │   │   ├── confluentkafka.py
    │           │   │   ├── consul.py
    │           │   │   ├── etcd.py
    │           │   │   ├── filesystem.py
    │           │   │   ├── gcpubsub.py
    │           │   │   ├── librabbitmq.py
    │           │   │   ├── memory.py
    │           │   │   ├── mongodb.py
    │           │   │   ├── native_delayed_delivery.py
    │           │   │   ├── pgmq.py
    │           │   │   ├── pyamqp.py
    │           │   │   ├── pyro.py
    │           │   │   ├── qpid.py
    │           │   │   ├── redis.py
    │           │   │   ├── sqlalchemy
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── models.py
    │           │   │   ├── virtual
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   └── exchange.py
    │           │   │   └── zookeeper.py
    │           │   └── utils
    │           │       ├── __init__.py
    │           │       ├── amq_manager.py
    │           │       ├── collections.py
    │           │       ├── compat.py
    │           │       ├── debug.py
    │           │       ├── div.py
    │           │       ├── encoding.py
    │           │       ├── eventio.py
    │           │       ├── functional.py
    │           │       ├── imports.py
    │           │       ├── json.py
    │           │       ├── limits.py
    │           │       ├── objects.py
    │           │       ├── scheduling.py
    │           │       ├── text.py
    │           │       ├── time.py
    │           │       ├── url.py
    │           │       └── uuid.py
    │           ├── kombu-5.7.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── loguru
    │           │   ├── __init__.py
    │           │   ├── __init__.pyi
    │           │   ├── _asyncio_loop.py
    │           │   ├── _better_exceptions.py
    │           │   ├── _colorama.py
    │           │   ├── _colorizer.py
    │           │   ├── _contextvars.py
    │           │   ├── _ctime_functions.py
    │           │   ├── _datetime.py
    │           │   ├── _defaults.py
    │           │   ├── _error_interceptor.py
    │           │   ├── _file_sink.py
    │           │   ├── _filters.py
    │           │   ├── _get_frame.py
    │           │   ├── _handler.py
    │           │   ├── _locks_machinery.py
    │           │   ├── _logger.py
    │           │   ├── _recattrs.py
    │           │   ├── _simple_sinks.py
    │           │   ├── _string_parsers.py
    │           │   └── py.typed
    │           ├── loguru-0.7.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   └── WHEEL
    │           ├── magic
    │           │   ├── __init__.py
    │           │   ├── __init__.pyi
    │           │   ├── compat.py
    │           │   ├── loader.py
    │           │   └── py.typed
    │           ├── mako
    │           │   ├── __init__.py
    │           │   ├── _ast_util.py
    │           │   ├── ast.py
    │           │   ├── cache.py
    │           │   ├── cmd.py
    │           │   ├── codegen.py
    │           │   ├── compat.py
    │           │   ├── exceptions.py
    │           │   ├── ext
    │           │   │   ├── __init__.py
    │           │   │   ├── autohandler.py
    │           │   │   ├── babelplugin.py
    │           │   │   ├── beaker_cache.py
    │           │   │   ├── extract.py
    │           │   │   ├── linguaplugin.py
    │           │   │   ├── preprocessors.py
    │           │   │   ├── pygmentplugin.py
    │           │   │   └── turbogears.py
    │           │   ├── filters.py
    │           │   ├── lexer.py
    │           │   ├── lookup.py
    │           │   ├── parsetree.py
    │           │   ├── pygen.py
    │           │   ├── pyparser.py
    │           │   ├── runtime.py
    │           │   ├── template.py
    │           │   ├── testing
    │           │   │   ├── __init__.py
    │           │   │   ├── _config.py
    │           │   │   ├── assertions.py
    │           │   │   ├── config.py
    │           │   │   ├── exclusions.py
    │           │   │   ├── fixtures.py
    │           │   │   └── helpers.py
    │           │   └── util.py
    │           ├── mako-1.4.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── markupsafe
    │           │   ├── __init__.py
    │           │   ├── _native.py
    │           │   ├── _speedups.c
    │           │   ├── _speedups.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _speedups.pyi
    │           │   └── py.typed
    │           ├── markupsafe-3.0.4.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── mmh3
    │           │   ├── __init__.pyi
    │           │   ├── hashlib.h
    │           │   ├── mmh3module.c
    │           │   ├── murmurhash3.c
    │           │   ├── murmurhash3.h
    │           │   └── py.typed
    │           ├── mmh3-5.3.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── mmh3.cpython-314-x86_64-linux-gnu.so
    │           ├── multipart
    │           │   ├── __init__.py
    │           │   ├── decoders.py
    │           │   ├── exceptions.py
    │           │   └── multipart.py
    │           ├── networkx
    │           │   ├── __init__.py
    │           │   ├── algorithms
    │           │   │   ├── __init__.py
    │           │   │   ├── approximation
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── clique.py
    │           │   │   │   ├── clustering_coefficient.py
    │           │   │   │   ├── connectivity.py
    │           │   │   │   ├── density.py
    │           │   │   │   ├── distance_measures.py
    │           │   │   │   ├── dominating_set.py
    │           │   │   │   ├── kcomponents.py
    │           │   │   │   ├── matching.py
    │           │   │   │   ├── maxcut.py
    │           │   │   │   ├── ramsey.py
    │           │   │   │   ├── steinertree.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_approx_clust_coeff.py
    │           │   │   │   │   ├── test_clique.py
    │           │   │   │   │   ├── test_connectivity.py
    │           │   │   │   │   ├── test_density.py
    │           │   │   │   │   ├── test_distance_measures.py
    │           │   │   │   │   ├── test_dominating_set.py
    │           │   │   │   │   ├── test_kcomponents.py
    │           │   │   │   │   ├── test_matching.py
    │           │   │   │   │   ├── test_maxcut.py
    │           │   │   │   │   ├── test_ramsey.py
    │           │   │   │   │   ├── test_steinertree.py
    │           │   │   │   │   ├── test_traveling_salesman.py
    │           │   │   │   │   ├── test_treewidth.py
    │           │   │   │   │   └── test_vertex_cover.py
    │           │   │   │   ├── traveling_salesman.py
    │           │   │   │   ├── treewidth.py
    │           │   │   │   └── vertex_cover.py
    │           │   │   ├── assortativity
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── connectivity.py
    │           │   │   │   ├── correlation.py
    │           │   │   │   ├── mixing.py
    │           │   │   │   ├── neighbor_degree.py
    │           │   │   │   ├── pairs.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── base_test.py
    │           │   │   │       ├── test_connectivity.py
    │           │   │   │       ├── test_correlation.py
    │           │   │   │       ├── test_mixing.py
    │           │   │   │       ├── test_neighbor_degree.py
    │           │   │   │       └── test_pairs.py
    │           │   │   ├── asteroidal.py
    │           │   │   ├── bipartite
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── basic.py
    │           │   │   │   ├── centrality.py
    │           │   │   │   ├── cluster.py
    │           │   │   │   ├── community.py
    │           │   │   │   ├── covering.py
    │           │   │   │   ├── edgelist.py
    │           │   │   │   ├── extendability.py
    │           │   │   │   ├── generators.py
    │           │   │   │   ├── link_analysis.py
    │           │   │   │   ├── matching.py
    │           │   │   │   ├── matrix.py
    │           │   │   │   ├── projection.py
    │           │   │   │   ├── redundancy.py
    │           │   │   │   ├── spectral.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_basic.py
    │           │   │   │       ├── test_centrality.py
    │           │   │   │       ├── test_cluster.py
    │           │   │   │       ├── test_community.py
    │           │   │   │       ├── test_covering.py
    │           │   │   │       ├── test_edgelist.py
    │           │   │   │       ├── test_extendability.py
    │           │   │   │       ├── test_generators.py
    │           │   │   │       ├── test_link_analysis.py
    │           │   │   │       ├── test_matching.py
    │           │   │   │       ├── test_matrix.py
    │           │   │   │       ├── test_project.py
    │           │   │   │       ├── test_redundancy.py
    │           │   │   │       └── test_spectral_bipartivity.py
    │           │   │   ├── boundary.py
    │           │   │   ├── bridges.py
    │           │   │   ├── broadcasting.py
    │           │   │   ├── centrality
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── betweenness.py
    │           │   │   │   ├── betweenness_subset.py
    │           │   │   │   ├── closeness.py
    │           │   │   │   ├── current_flow_betweenness.py
    │           │   │   │   ├── current_flow_betweenness_subset.py
    │           │   │   │   ├── current_flow_closeness.py
    │           │   │   │   ├── degree_alg.py
    │           │   │   │   ├── dispersion.py
    │           │   │   │   ├── eigenvector.py
    │           │   │   │   ├── flow_matrix.py
    │           │   │   │   ├── group.py
    │           │   │   │   ├── harmonic.py
    │           │   │   │   ├── katz.py
    │           │   │   │   ├── laplacian.py
    │           │   │   │   ├── load.py
    │           │   │   │   ├── percolation.py
    │           │   │   │   ├── reaching.py
    │           │   │   │   ├── second_order.py
    │           │   │   │   ├── subgraph_alg.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_betweenness_centrality.py
    │           │   │   │   │   ├── test_betweenness_centrality_subset.py
    │           │   │   │   │   ├── test_closeness_centrality.py
    │           │   │   │   │   ├── test_current_flow_betweenness_centrality.py
    │           │   │   │   │   ├── test_current_flow_betweenness_centrality_subset.py
    │           │   │   │   │   ├── test_current_flow_closeness.py
    │           │   │   │   │   ├── test_degree_centrality.py
    │           │   │   │   │   ├── test_dispersion.py
    │           │   │   │   │   ├── test_eigenvector_centrality.py
    │           │   │   │   │   ├── test_group.py
    │           │   │   │   │   ├── test_harmonic_centrality.py
    │           │   │   │   │   ├── test_katz_centrality.py
    │           │   │   │   │   ├── test_laplacian_centrality.py
    │           │   │   │   │   ├── test_load_centrality.py
    │           │   │   │   │   ├── test_percolation_centrality.py
    │           │   │   │   │   ├── test_reaching.py
    │           │   │   │   │   ├── test_second_order_centrality.py
    │           │   │   │   │   ├── test_subgraph.py
    │           │   │   │   │   ├── test_trophic.py
    │           │   │   │   │   └── test_voterank.py
    │           │   │   │   ├── trophic.py
    │           │   │   │   └── voterank_alg.py
    │           │   │   ├── chains.py
    │           │   │   ├── chordal.py
    │           │   │   ├── clique.py
    │           │   │   ├── cluster.py
    │           │   │   ├── coloring
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── equitable_coloring.py
    │           │   │   │   ├── greedy_coloring.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       └── test_coloring.py
    │           │   │   ├── communicability_alg.py
    │           │   │   ├── community
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── asyn_fluid.py
    │           │   │   │   ├── bipartitions.py
    │           │   │   │   ├── centrality.py
    │           │   │   │   ├── community_utils.py
    │           │   │   │   ├── divisive.py
    │           │   │   │   ├── kclique.py
    │           │   │   │   ├── label_propagation.py
    │           │   │   │   ├── leiden.py
    │           │   │   │   ├── local.py
    │           │   │   │   ├── louvain.py
    │           │   │   │   ├── lukes.py
    │           │   │   │   ├── modularity_max.py
    │           │   │   │   ├── quality.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_asyn_fluid.py
    │           │   │   │       ├── test_bipartitions.py
    │           │   │   │       ├── test_centrality.py
    │           │   │   │       ├── test_divisive.py
    │           │   │   │       ├── test_kclique.py
    │           │   │   │       ├── test_label_propagation.py
    │           │   │   │       ├── test_leiden.py
    │           │   │   │       ├── test_local.py
    │           │   │   │       ├── test_louvain.py
    │           │   │   │       ├── test_lukes.py
    │           │   │   │       ├── test_modularity_max.py
    │           │   │   │       ├── test_quality.py
    │           │   │   │       └── test_utils.py
    │           │   │   ├── components
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── attracting.py
    │           │   │   │   ├── biconnected.py
    │           │   │   │   ├── connected.py
    │           │   │   │   ├── semiconnected.py
    │           │   │   │   ├── strongly_connected.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_attracting.py
    │           │   │   │   │   ├── test_biconnected.py
    │           │   │   │   │   ├── test_connected.py
    │           │   │   │   │   ├── test_semiconnected.py
    │           │   │   │   │   ├── test_strongly_connected.py
    │           │   │   │   │   └── test_weakly_connected.py
    │           │   │   │   └── weakly_connected.py
    │           │   │   ├── connectivity
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── connectivity.py
    │           │   │   │   ├── cuts.py
    │           │   │   │   ├── disjoint_paths.py
    │           │   │   │   ├── edge_augmentation.py
    │           │   │   │   ├── edge_kcomponents.py
    │           │   │   │   ├── kcomponents.py
    │           │   │   │   ├── kcutsets.py
    │           │   │   │   ├── stoerwagner.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_connectivity.py
    │           │   │   │   │   ├── test_cuts.py
    │           │   │   │   │   ├── test_disjoint_paths.py
    │           │   │   │   │   ├── test_edge_augmentation.py
    │           │   │   │   │   ├── test_edge_kcomponents.py
    │           │   │   │   │   ├── test_kcomponents.py
    │           │   │   │   │   ├── test_kcutsets.py
    │           │   │   │   │   └── test_stoer_wagner.py
    │           │   │   │   └── utils.py
    │           │   │   ├── core.py
    │           │   │   ├── covering.py
    │           │   │   ├── cuts.py
    │           │   │   ├── cycles.py
    │           │   │   ├── d_separation.py
    │           │   │   ├── dag.py
    │           │   │   ├── distance_measures.py
    │           │   │   ├── distance_regular.py
    │           │   │   ├── dominance.py
    │           │   │   ├── dominating.py
    │           │   │   ├── efficiency_measures.py
    │           │   │   ├── euler.py
    │           │   │   ├── flow
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── boykovkolmogorov.py
    │           │   │   │   ├── capacityscaling.py
    │           │   │   │   ├── dinitz_alg.py
    │           │   │   │   ├── edmondskarp.py
    │           │   │   │   ├── gomory_hu.py
    │           │   │   │   ├── maxflow.py
    │           │   │   │   ├── mincost.py
    │           │   │   │   ├── networksimplex.py
    │           │   │   │   ├── preflowpush.py
    │           │   │   │   ├── shortestaugmentingpath.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── gl1.gpickle.bz2
    │           │   │   │   │   ├── gw1.gpickle.bz2
    │           │   │   │   │   ├── netgen-2.gpickle.bz2
    │           │   │   │   │   ├── test_gomory_hu.py
    │           │   │   │   │   ├── test_maxflow.py
    │           │   │   │   │   ├── test_maxflow_large_graph.py
    │           │   │   │   │   ├── test_mincost.py
    │           │   │   │   │   ├── test_networksimplex.py
    │           │   │   │   │   └── wlm3.gpickle.bz2
    │           │   │   │   └── utils.py
    │           │   │   ├── graph_hashing.py
    │           │   │   ├── graphical.py
    │           │   │   ├── hierarchy.py
    │           │   │   ├── hybrid.py
    │           │   │   ├── isolate.py
    │           │   │   ├── isomorphism
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── ismags.py
    │           │   │   │   ├── isomorph.py
    │           │   │   │   ├── isomorphvf2.py
    │           │   │   │   ├── matchhelpers.py
    │           │   │   │   ├── temporalisomorphvf2.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── iso_r01_s80.A99
    │           │   │   │   │   ├── iso_r01_s80.B99
    │           │   │   │   │   ├── si2_b06_m200.A99
    │           │   │   │   │   ├── si2_b06_m200.B99
    │           │   │   │   │   ├── test_common.py
    │           │   │   │   │   ├── test_ismags.py
    │           │   │   │   │   ├── test_isomorphism.py
    │           │   │   │   │   ├── test_isomorphvf2.py
    │           │   │   │   │   ├── test_match_helpers.py
    │           │   │   │   │   ├── test_temporalisomorphvf2.py
    │           │   │   │   │   ├── test_tree_isomorphism.py
    │           │   │   │   │   ├── test_vf2pp.py
    │           │   │   │   │   ├── test_vf2pp_helpers.py
    │           │   │   │   │   └── test_vf2userfunc.py
    │           │   │   │   ├── tree_isomorphism.py
    │           │   │   │   ├── vf2pp.py
    │           │   │   │   └── vf2userfunc.py
    │           │   │   ├── link_analysis
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── hits_alg.py
    │           │   │   │   ├── pagerank_alg.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_hits.py
    │           │   │   │       └── test_pagerank.py
    │           │   │   ├── link_prediction.py
    │           │   │   ├── lowest_common_ancestors.py
    │           │   │   ├── matching.py
    │           │   │   ├── minors
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── contraction.py
    │           │   │   │   └── tests
    │           │   │   │       └── test_contraction.py
    │           │   │   ├── mis.py
    │           │   │   ├── moral.py
    │           │   │   ├── node_classification.py
    │           │   │   ├── non_randomness.py
    │           │   │   ├── operators
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── all.py
    │           │   │   │   ├── binary.py
    │           │   │   │   ├── product.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_all.py
    │           │   │   │   │   ├── test_binary.py
    │           │   │   │   │   ├── test_product.py
    │           │   │   │   │   └── test_unary.py
    │           │   │   │   └── unary.py
    │           │   │   ├── perfect_graph.py
    │           │   │   ├── planar_drawing.py
    │           │   │   ├── planarity.py
    │           │   │   ├── polynomials.py
    │           │   │   ├── reciprocity.py
    │           │   │   ├── regular.py
    │           │   │   ├── richclub.py
    │           │   │   ├── shortest_paths
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── astar.py
    │           │   │   │   ├── dense.py
    │           │   │   │   ├── generic.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_astar.py
    │           │   │   │   │   ├── test_dense.py
    │           │   │   │   │   ├── test_dense_numpy.py
    │           │   │   │   │   ├── test_generic.py
    │           │   │   │   │   ├── test_unweighted.py
    │           │   │   │   │   └── test_weighted.py
    │           │   │   │   ├── unweighted.py
    │           │   │   │   └── weighted.py
    │           │   │   ├── similarity.py
    │           │   │   ├── simple_paths.py
    │           │   │   ├── smallworld.py
    │           │   │   ├── smetric.py
    │           │   │   ├── sparsifiers.py
    │           │   │   ├── structuralholes.py
    │           │   │   ├── summarization.py
    │           │   │   ├── swap.py
    │           │   │   ├── tests
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_asteroidal.py
    │           │   │   │   ├── test_boundary.py
    │           │   │   │   ├── test_bridges.py
    │           │   │   │   ├── test_broadcasting.py
    │           │   │   │   ├── test_chains.py
    │           │   │   │   ├── test_chordal.py
    │           │   │   │   ├── test_clique.py
    │           │   │   │   ├── test_cluster.py
    │           │   │   │   ├── test_communicability.py
    │           │   │   │   ├── test_core.py
    │           │   │   │   ├── test_covering.py
    │           │   │   │   ├── test_cuts.py
    │           │   │   │   ├── test_cycles.py
    │           │   │   │   ├── test_d_separation.py
    │           │   │   │   ├── test_dag.py
    │           │   │   │   ├── test_distance_measures.py
    │           │   │   │   ├── test_distance_regular.py
    │           │   │   │   ├── test_dominance.py
    │           │   │   │   ├── test_dominating.py
    │           │   │   │   ├── test_efficiency.py
    │           │   │   │   ├── test_euler.py
    │           │   │   │   ├── test_graph_hashing.py
    │           │   │   │   ├── test_graphical.py
    │           │   │   │   ├── test_hierarchy.py
    │           │   │   │   ├── test_hybrid.py
    │           │   │   │   ├── test_isolate.py
    │           │   │   │   ├── test_link_prediction.py
    │           │   │   │   ├── test_lowest_common_ancestors.py
    │           │   │   │   ├── test_matching.py
    │           │   │   │   ├── test_max_weight_clique.py
    │           │   │   │   ├── test_mis.py
    │           │   │   │   ├── test_moral.py
    │           │   │   │   ├── test_node_classification.py
    │           │   │   │   ├── test_non_randomness.py
    │           │   │   │   ├── test_perfect_graph.py
    │           │   │   │   ├── test_planar_drawing.py
    │           │   │   │   ├── test_planarity.py
    │           │   │   │   ├── test_polynomials.py
    │           │   │   │   ├── test_reciprocity.py
    │           │   │   │   ├── test_regular.py
    │           │   │   │   ├── test_richclub.py
    │           │   │   │   ├── test_similarity.py
    │           │   │   │   ├── test_simple_paths.py
    │           │   │   │   ├── test_smallworld.py
    │           │   │   │   ├── test_smetric.py
    │           │   │   │   ├── test_sparsifiers.py
    │           │   │   │   ├── test_structuralholes.py
    │           │   │   │   ├── test_summarization.py
    │           │   │   │   ├── test_swap.py
    │           │   │   │   ├── test_threshold.py
    │           │   │   │   ├── test_time_dependent.py
    │           │   │   │   ├── test_tournament.py
    │           │   │   │   ├── test_triads.py
    │           │   │   │   ├── test_vitality.py
    │           │   │   │   ├── test_voronoi.py
    │           │   │   │   ├── test_walks.py
    │           │   │   │   └── test_wiener.py
    │           │   │   ├── threshold.py
    │           │   │   ├── time_dependent.py
    │           │   │   ├── tournament.py
    │           │   │   ├── traversal
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── beamsearch.py
    │           │   │   │   ├── breadth_first_search.py
    │           │   │   │   ├── depth_first_search.py
    │           │   │   │   ├── edgebfs.py
    │           │   │   │   ├── edgedfs.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_beamsearch.py
    │           │   │   │       ├── test_bfs.py
    │           │   │   │       ├── test_dfs.py
    │           │   │   │       ├── test_edgebfs.py
    │           │   │   │       └── test_edgedfs.py
    │           │   │   ├── tree
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── branchings.py
    │           │   │   │   ├── coding.py
    │           │   │   │   ├── decomposition.py
    │           │   │   │   ├── distance_measures.py
    │           │   │   │   ├── mst.py
    │           │   │   │   ├── operations.py
    │           │   │   │   ├── recognition.py
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_branchings.py
    │           │   │   │       ├── test_coding.py
    │           │   │   │       ├── test_decomposition.py
    │           │   │   │       ├── test_distance_measures.py
    │           │   │   │       ├── test_mst.py
    │           │   │   │       ├── test_operations.py
    │           │   │   │       └── test_recognition.py
    │           │   │   ├── triads.py
    │           │   │   ├── vitality.py
    │           │   │   ├── voronoi.py
    │           │   │   ├── walks.py
    │           │   │   └── wiener.py
    │           │   ├── classes
    │           │   │   ├── __init__.py
    │           │   │   ├── coreviews.py
    │           │   │   ├── digraph.py
    │           │   │   ├── filters.py
    │           │   │   ├── function.py
    │           │   │   ├── graph.py
    │           │   │   ├── graphviews.py
    │           │   │   ├── multidigraph.py
    │           │   │   ├── multigraph.py
    │           │   │   ├── reportviews.py
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── dispatch_interface.py
    │           │   │       ├── historical_tests.py
    │           │   │       ├── test_coreviews.py
    │           │   │       ├── test_digraph.py
    │           │   │       ├── test_digraph_historical.py
    │           │   │       ├── test_filters.py
    │           │   │       ├── test_function.py
    │           │   │       ├── test_graph.py
    │           │   │       ├── test_graph_historical.py
    │           │   │       ├── test_graphviews.py
    │           │   │       ├── test_multidigraph.py
    │           │   │       ├── test_multigraph.py
    │           │   │       ├── test_reportviews.py
    │           │   │       ├── test_special.py
    │           │   │       └── test_subgraphviews.py
    │           │   ├── conftest.py
    │           │   ├── convert.py
    │           │   ├── convert_matrix.py
    │           │   ├── drawing
    │           │   │   ├── __init__.py
    │           │   │   ├── layout.py
    │           │   │   ├── nx_agraph.py
    │           │   │   ├── nx_latex.py
    │           │   │   ├── nx_pydot.py
    │           │   │   ├── nx_pylab.py
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── baseline
    │           │   │       │   ├── test_display_complex.png
    │           │   │       │   ├── test_display_empty_graph.png
    │           │   │       │   ├── test_display_house_with_colors.png
    │           │   │       │   ├── test_display_labels_and_colors.png
    │           │   │       │   ├── test_display_shortest_path.png
    │           │   │       │   └── test_house_with_colors.png
    │           │   │       ├── test_agraph.py
    │           │   │       ├── test_image_comparison_pylab_mpl.py
    │           │   │       ├── test_latex.py
    │           │   │       ├── test_layout.py
    │           │   │       ├── test_pydot.py
    │           │   │       └── test_pylab.py
    │           │   ├── exception.py
    │           │   ├── generators
    │           │   │   ├── __init__.py
    │           │   │   ├── atlas.dat.gz
    │           │   │   ├── atlas.py
    │           │   │   ├── classic.py
    │           │   │   ├── cographs.py
    │           │   │   ├── community.py
    │           │   │   ├── degree_seq.py
    │           │   │   ├── directed.py
    │           │   │   ├── duplication.py
    │           │   │   ├── ego.py
    │           │   │   ├── expanders.py
    │           │   │   ├── geometric.py
    │           │   │   ├── harary_graph.py
    │           │   │   ├── internet_as_graphs.py
    │           │   │   ├── intersection.py
    │           │   │   ├── interval_graph.py
    │           │   │   ├── joint_degree_seq.py
    │           │   │   ├── lattice.py
    │           │   │   ├── line.py
    │           │   │   ├── mycielski.py
    │           │   │   ├── nonisomorphic_trees.py
    │           │   │   ├── random_clustered.py
    │           │   │   ├── random_graphs.py
    │           │   │   ├── small.py
    │           │   │   ├── social.py
    │           │   │   ├── spectral_graph_forge.py
    │           │   │   ├── stochastic.py
    │           │   │   ├── sudoku.py
    │           │   │   ├── tests
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_atlas.py
    │           │   │   │   ├── test_classic.py
    │           │   │   │   ├── test_cographs.py
    │           │   │   │   ├── test_community.py
    │           │   │   │   ├── test_degree_seq.py
    │           │   │   │   ├── test_directed.py
    │           │   │   │   ├── test_duplication.py
    │           │   │   │   ├── test_ego.py
    │           │   │   │   ├── test_expanders.py
    │           │   │   │   ├── test_geometric.py
    │           │   │   │   ├── test_harary_graph.py
    │           │   │   │   ├── test_internet_as_graphs.py
    │           │   │   │   ├── test_intersection.py
    │           │   │   │   ├── test_interval_graph.py
    │           │   │   │   ├── test_joint_degree_seq.py
    │           │   │   │   ├── test_lattice.py
    │           │   │   │   ├── test_line.py
    │           │   │   │   ├── test_mycielski.py
    │           │   │   │   ├── test_nonisomorphic_trees.py
    │           │   │   │   ├── test_random_clustered.py
    │           │   │   │   ├── test_random_graphs.py
    │           │   │   │   ├── test_small.py
    │           │   │   │   ├── test_spectral_graph_forge.py
    │           │   │   │   ├── test_stochastic.py
    │           │   │   │   ├── test_sudoku.py
    │           │   │   │   ├── test_time_series.py
    │           │   │   │   ├── test_trees.py
    │           │   │   │   └── test_triads.py
    │           │   │   ├── time_series.py
    │           │   │   ├── trees.py
    │           │   │   └── triads.py
    │           │   ├── lazy_imports.py
    │           │   ├── linalg
    │           │   │   ├── __init__.py
    │           │   │   ├── algebraicconnectivity.py
    │           │   │   ├── attrmatrix.py
    │           │   │   ├── bethehessianmatrix.py
    │           │   │   ├── graphmatrix.py
    │           │   │   ├── laplacianmatrix.py
    │           │   │   ├── modularitymatrix.py
    │           │   │   ├── spectrum.py
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── test_algebraic_connectivity.py
    │           │   │       ├── test_attrmatrix.py
    │           │   │       ├── test_bethehessian.py
    │           │   │       ├── test_graphmatrix.py
    │           │   │       ├── test_laplacian.py
    │           │   │       ├── test_modularity.py
    │           │   │       └── test_spectrum.py
    │           │   ├── readwrite
    │           │   │   ├── __init__.py
    │           │   │   ├── adjlist.py
    │           │   │   ├── edgelist.py
    │           │   │   ├── gexf.py
    │           │   │   ├── gml.py
    │           │   │   ├── graph6.py
    │           │   │   ├── graphml.py
    │           │   │   ├── json_graph
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── adjacency.py
    │           │   │   │   ├── cytoscape.py
    │           │   │   │   ├── node_link.py
    │           │   │   │   ├── tests
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_adjacency.py
    │           │   │   │   │   ├── test_cytoscape.py
    │           │   │   │   │   ├── test_node_link.py
    │           │   │   │   │   └── test_tree.py
    │           │   │   │   └── tree.py
    │           │   │   ├── leda.py
    │           │   │   ├── multiline_adjlist.py
    │           │   │   ├── p2g.py
    │           │   │   ├── pajek.py
    │           │   │   ├── sparse6.py
    │           │   │   ├── tests
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_adjlist.py
    │           │   │   │   ├── test_edgelist.py
    │           │   │   │   ├── test_gexf.py
    │           │   │   │   ├── test_gml.py
    │           │   │   │   ├── test_graph6.py
    │           │   │   │   ├── test_graphml.py
    │           │   │   │   ├── test_leda.py
    │           │   │   │   ├── test_p2g.py
    │           │   │   │   ├── test_pajek.py
    │           │   │   │   ├── test_sparse6.py
    │           │   │   │   └── test_text.py
    │           │   │   └── text.py
    │           │   ├── relabel.py
    │           │   ├── tests
    │           │   │   ├── __init__.py
    │           │   │   ├── test_all_random_functions.py
    │           │   │   ├── test_convert.py
    │           │   │   ├── test_convert_numpy.py
    │           │   │   ├── test_convert_pandas.py
    │           │   │   ├── test_convert_scipy.py
    │           │   │   ├── test_exceptions.py
    │           │   │   ├── test_import.py
    │           │   │   ├── test_lazy_imports.py
    │           │   │   ├── test_relabel.py
    │           │   │   └── test_removed_functions_exception_messages.py
    │           │   └── utils
    │           │       ├── __init__.py
    │           │       ├── backends.py
    │           │       ├── configs.py
    │           │       ├── decorators.py
    │           │       ├── heaps.py
    │           │       ├── mapped_queue.py
    │           │       ├── misc.py
    │           │       ├── random_sequence.py
    │           │       ├── rcm.py
    │           │       ├── tests
    │           │       │   ├── __init__.py
    │           │       │   ├── test__init.py
    │           │       │   ├── test_backends.py
    │           │       │   ├── test_config.py
    │           │       │   ├── test_decorators.py
    │           │       │   ├── test_heaps.py
    │           │       │   ├── test_mapped_queue.py
    │           │       │   ├── test_misc.py
    │           │       │   ├── test_random_sequence.py
    │           │       │   ├── test_rcm.py
    │           │       │   └── test_unionfind.py
    │           │       └── union_find.py
    │           ├── networkx-3.7.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── numpy
    │           │   ├── __config__.py
    │           │   ├── __config__.pyi
    │           │   ├── __init__.cython-30.pxd
    │           │   ├── __init__.pxd
    │           │   ├── __init__.py
    │           │   ├── __init__.pyi
    │           │   ├── _array_api_info.py
    │           │   ├── _array_api_info.pyi
    │           │   ├── _configtool.py
    │           │   ├── _configtool.pyi
    │           │   ├── _core
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _add_newdocs.py
    │           │   │   ├── _add_newdocs.pyi
    │           │   │   ├── _add_newdocs_scalars.py
    │           │   │   ├── _add_newdocs_scalars.pyi
    │           │   │   ├── _asarray.py
    │           │   │   ├── _asarray.pyi
    │           │   │   ├── _dtype.py
    │           │   │   ├── _dtype.pyi
    │           │   │   ├── _dtype_ctypes.py
    │           │   │   ├── _dtype_ctypes.pyi
    │           │   │   ├── _exceptions.py
    │           │   │   ├── _exceptions.pyi
    │           │   │   ├── _internal.py
    │           │   │   ├── _internal.pyi
    │           │   │   ├── _methods.py
    │           │   │   ├── _methods.pyi
    │           │   │   ├── _multiarray_tests.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _multiarray_umath.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _operand_flag_tests.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _rational_tests.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _simd.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _simd.pyi
    │           │   │   ├── _string_helpers.py
    │           │   │   ├── _string_helpers.pyi
    │           │   │   ├── _struct_ufunc_tests.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _type_aliases.py
    │           │   │   ├── _type_aliases.pyi
    │           │   │   ├── _ufunc_config.py
    │           │   │   ├── _ufunc_config.pyi
    │           │   │   ├── _umath_tests.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _umath_tests.pyi
    │           │   │   ├── arrayprint.py
    │           │   │   ├── arrayprint.pyi
    │           │   │   ├── cversions.py
    │           │   │   ├── defchararray.py
    │           │   │   ├── defchararray.pyi
    │           │   │   ├── einsumfunc.py
    │           │   │   ├── einsumfunc.pyi
    │           │   │   ├── fromnumeric.py
    │           │   │   ├── fromnumeric.pyi
    │           │   │   ├── function_base.py
    │           │   │   ├── function_base.pyi
    │           │   │   ├── getlimits.py
    │           │   │   ├── getlimits.pyi
    │           │   │   ├── include
    │           │   │   │   └── numpy
    │           │   │   │       ├── __multiarray_api.c
    │           │   │   │       ├── __multiarray_api.h
    │           │   │   │       ├── __ufunc_api.c
    │           │   │   │       ├── __ufunc_api.h
    │           │   │   │       ├── _neighborhood_iterator_imp.h
    │           │   │   │       ├── _numpyconfig.h
    │           │   │   │       ├── _public_dtype_api_table.h
    │           │   │   │       ├── arrayobject.h
    │           │   │   │       ├── arrayscalars.h
    │           │   │   │       ├── dtype_api.h
    │           │   │   │       ├── halffloat.h
    │           │   │   │       ├── ndarrayobject.h
    │           │   │   │       ├── ndarraytypes.h
    │           │   │   │       ├── npy_2_compat.h
    │           │   │   │       ├── npy_2_complexcompat.h
    │           │   │   │       ├── npy_3kcompat.h
    │           │   │   │       ├── npy_common.h
    │           │   │   │       ├── npy_cpu.h
    │           │   │   │       ├── npy_endian.h
    │           │   │   │       ├── npy_math.h
    │           │   │   │       ├── npy_no_deprecated_api.h
    │           │   │   │       ├── npy_os.h
    │           │   │   │       ├── numpyconfig.h
    │           │   │   │       ├── random
    │           │   │   │       │   ├── LICENSE.txt
    │           │   │   │       │   ├── bitgen.h
    │           │   │   │       │   ├── distributions.h
    │           │   │   │       │   └── libdivide.h
    │           │   │   │       ├── ufuncobject.h
    │           │   │   │       └── utils.h
    │           │   │   ├── lib
    │           │   │   │   ├── libnpymath.a
    │           │   │   │   └── pkgconfig
    │           │   │   │       └── numpy.pc
    │           │   │   ├── memmap.py
    │           │   │   ├── memmap.pyi
    │           │   │   ├── multiarray.py
    │           │   │   ├── multiarray.pyi
    │           │   │   ├── numeric.py
    │           │   │   ├── numeric.pyi
    │           │   │   ├── numerictypes.py
    │           │   │   ├── numerictypes.pyi
    │           │   │   ├── overrides.py
    │           │   │   ├── overrides.pyi
    │           │   │   ├── printoptions.py
    │           │   │   ├── printoptions.pyi
    │           │   │   ├── records.py
    │           │   │   ├── records.pyi
    │           │   │   ├── shape_base.py
    │           │   │   ├── shape_base.pyi
    │           │   │   ├── strings.py
    │           │   │   ├── strings.pyi
    │           │   │   ├── tests
    │           │   │   │   ├── _locales.py
    │           │   │   │   ├── _natype.py
    │           │   │   │   ├── data
    │           │   │   │   │   ├── astype_copy.pkl
    │           │   │   │   │   ├── generate_umath_validation_data.cpp
    │           │   │   │   │   ├── recarray_from_file.fits
    │           │   │   │   │   ├── umath-validation-set-README.txt
    │           │   │   │   │   ├── umath-validation-set-arccos.csv
    │           │   │   │   │   ├── umath-validation-set-arccosh.csv
    │           │   │   │   │   ├── umath-validation-set-arcsin.csv
    │           │   │   │   │   ├── umath-validation-set-arcsinh.csv
    │           │   │   │   │   ├── umath-validation-set-arctan.csv
    │           │   │   │   │   ├── umath-validation-set-arctanh.csv
    │           │   │   │   │   ├── umath-validation-set-cbrt.csv
    │           │   │   │   │   ├── umath-validation-set-cos.csv
    │           │   │   │   │   ├── umath-validation-set-cosh.csv
    │           │   │   │   │   ├── umath-validation-set-exp.csv
    │           │   │   │   │   ├── umath-validation-set-exp2.csv
    │           │   │   │   │   ├── umath-validation-set-expm1.csv
    │           │   │   │   │   ├── umath-validation-set-log.csv
    │           │   │   │   │   ├── umath-validation-set-log10.csv
    │           │   │   │   │   ├── umath-validation-set-log1p.csv
    │           │   │   │   │   ├── umath-validation-set-log2.csv
    │           │   │   │   │   ├── umath-validation-set-sin.csv
    │           │   │   │   │   ├── umath-validation-set-sinh.csv
    │           │   │   │   │   ├── umath-validation-set-tan.csv
    │           │   │   │   │   └── umath-validation-set-tanh.csv
    │           │   │   │   ├── examples
    │           │   │   │   │   ├── cython
    │           │   │   │   │   │   ├── checks.pyx
    │           │   │   │   │   │   ├── meson.build
    │           │   │   │   │   │   └── setup.py
    │           │   │   │   │   └── limited_api
    │           │   │   │   │       ├── limited_api.c
    │           │   │   │   │       ├── limited_api_cython.pyx
    │           │   │   │   │       ├── meson.build
    │           │   │   │   │       └── setup.py
    │           │   │   │   ├── test__exceptions.py
    │           │   │   │   ├── test_abc.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   ├── test_argparse.py
    │           │   │   │   ├── test_array_api_info.py
    │           │   │   │   ├── test_array_coercion.py
    │           │   │   │   ├── test_array_interface.py
    │           │   │   │   ├── test_arraymethod.py
    │           │   │   │   ├── test_arrayobject.py
    │           │   │   │   ├── test_arrayprint.py
    │           │   │   │   ├── test_casting_floatingpoint_errors.py
    │           │   │   │   ├── test_casting_unittests.py
    │           │   │   │   ├── test_conversion_utils.py
    │           │   │   │   ├── test_cpu_dispatcher.py
    │           │   │   │   ├── test_cpu_features.py
    │           │   │   │   ├── test_custom_dtypes.py
    │           │   │   │   ├── test_cython.py
    │           │   │   │   ├── test_datetime.py
    │           │   │   │   ├── test_defchararray.py
    │           │   │   │   ├── test_deprecations.py
    │           │   │   │   ├── test_dlpack.py
    │           │   │   │   ├── test_dtype.py
    │           │   │   │   ├── test_einsum.py
    │           │   │   │   ├── test_errstate.py
    │           │   │   │   ├── test_extint128.py
    │           │   │   │   ├── test_finfo.py
    │           │   │   │   ├── test_function_base.py
    │           │   │   │   ├── test_getlimits.py
    │           │   │   │   ├── test_half.py
    │           │   │   │   ├── test_hashtable.py
    │           │   │   │   ├── test_indexerrors.py
    │           │   │   │   ├── test_indexing.py
    │           │   │   │   ├── test_item_selection.py
    │           │   │   │   ├── test_limited_api.py
    │           │   │   │   ├── test_longdouble.py
    │           │   │   │   ├── test_mem_overlap.py
    │           │   │   │   ├── test_mem_policy.py
    │           │   │   │   ├── test_memmap.py
    │           │   │   │   ├── test_multiarray.py
    │           │   │   │   ├── test_multiprocessing.py
    │           │   │   │   ├── test_multithreading.py
    │           │   │   │   ├── test_nditer.py
    │           │   │   │   ├── test_nep50_promotions.py
    │           │   │   │   ├── test_numeric.py
    │           │   │   │   ├── test_numerictypes.py
    │           │   │   │   ├── test_overrides.py
    │           │   │   │   ├── test_print.py
    │           │   │   │   ├── test_protocols.py
    │           │   │   │   ├── test_records.py
    │           │   │   │   ├── test_regression.py
    │           │   │   │   ├── test_scalar_ctors.py
    │           │   │   │   ├── test_scalar_methods.py
    │           │   │   │   ├── test_scalarbuffer.py
    │           │   │   │   ├── test_scalarinherit.py
    │           │   │   │   ├── test_scalarmath.py
    │           │   │   │   ├── test_scalarprint.py
    │           │   │   │   ├── test_shape_base.py
    │           │   │   │   ├── test_simd.py
    │           │   │   │   ├── test_simd_module.py
    │           │   │   │   ├── test_stringdtype.py
    │           │   │   │   ├── test_strings.py
    │           │   │   │   ├── test_ufunc.py
    │           │   │   │   ├── test_umath.py
    │           │   │   │   ├── test_umath_accuracy.py
    │           │   │   │   ├── test_umath_complex.py
    │           │   │   │   └── test_unicode.py
    │           │   │   ├── umath.py
    │           │   │   └── umath.pyi
    │           │   ├── _distributor_init.py
    │           │   ├── _distributor_init.pyi
    │           │   ├── _expired_attrs_2_0.py
    │           │   ├── _expired_attrs_2_0.pyi
    │           │   ├── _globals.py
    │           │   ├── _globals.pyi
    │           │   ├── _pyinstaller
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── hook-numpy.py
    │           │   │   ├── hook-numpy.pyi
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── pyinstaller-smoke.py
    │           │   │       └── test_pyinstaller.py
    │           │   ├── _pytesttester.py
    │           │   ├── _pytesttester.pyi
    │           │   ├── _typing
    │           │   │   ├── __init__.py
    │           │   │   ├── _add_docstring.py
    │           │   │   ├── _array_like.py
    │           │   │   ├── _char_codes.py
    │           │   │   ├── _dtype_like.py
    │           │   │   ├── _extended_precision.py
    │           │   │   ├── _nbit.py
    │           │   │   ├── _nbit_base.py
    │           │   │   ├── _nbit_base.pyi
    │           │   │   ├── _nested_sequence.py
    │           │   │   ├── _scalars.py
    │           │   │   ├── _shape.py
    │           │   │   ├── _ufunc.py
    │           │   │   └── _ufunc.pyi
    │           │   ├── _utils
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _conversions.py
    │           │   │   ├── _conversions.pyi
    │           │   │   ├── _inspect.py
    │           │   │   ├── _inspect.pyi
    │           │   │   ├── _pep440.py
    │           │   │   └── _pep440.pyi
    │           │   ├── char
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── conftest.py
    │           │   ├── core
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _dtype.py
    │           │   │   ├── _dtype.pyi
    │           │   │   ├── _dtype_ctypes.py
    │           │   │   ├── _dtype_ctypes.pyi
    │           │   │   ├── _internal.py
    │           │   │   ├── _internal.pyi
    │           │   │   ├── _multiarray_umath.py
    │           │   │   ├── _utils.py
    │           │   │   ├── arrayprint.py
    │           │   │   ├── arrayprint.pyi
    │           │   │   ├── defchararray.py
    │           │   │   ├── defchararray.pyi
    │           │   │   ├── einsumfunc.py
    │           │   │   ├── einsumfunc.pyi
    │           │   │   ├── fromnumeric.py
    │           │   │   ├── fromnumeric.pyi
    │           │   │   ├── function_base.py
    │           │   │   ├── function_base.pyi
    │           │   │   ├── getlimits.py
    │           │   │   ├── getlimits.pyi
    │           │   │   ├── multiarray.py
    │           │   │   ├── multiarray.pyi
    │           │   │   ├── numeric.py
    │           │   │   ├── numeric.pyi
    │           │   │   ├── numerictypes.py
    │           │   │   ├── numerictypes.pyi
    │           │   │   ├── overrides.py
    │           │   │   ├── overrides.pyi
    │           │   │   ├── records.py
    │           │   │   ├── records.pyi
    │           │   │   ├── shape_base.py
    │           │   │   ├── shape_base.pyi
    │           │   │   ├── umath.py
    │           │   │   └── umath.pyi
    │           │   ├── ctypeslib
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _ctypeslib.py
    │           │   │   └── _ctypeslib.pyi
    │           │   ├── doc
    │           │   │   └── ufuncs.py
    │           │   ├── dtypes.py
    │           │   ├── dtypes.pyi
    │           │   ├── exceptions.py
    │           │   ├── exceptions.pyi
    │           │   ├── f2py
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── __main__.py
    │           │   │   ├── __version__.py
    │           │   │   ├── __version__.pyi
    │           │   │   ├── _backends
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __init__.pyi
    │           │   │   │   ├── _backend.py
    │           │   │   │   ├── _backend.pyi
    │           │   │   │   ├── _meson.py
    │           │   │   │   ├── _meson.pyi
    │           │   │   │   └── meson.build.template
    │           │   │   ├── _isocbind.py
    │           │   │   ├── _isocbind.pyi
    │           │   │   ├── _src_pyf.py
    │           │   │   ├── _src_pyf.pyi
    │           │   │   ├── auxfuncs.py
    │           │   │   ├── auxfuncs.pyi
    │           │   │   ├── capi_maps.py
    │           │   │   ├── capi_maps.pyi
    │           │   │   ├── cb_rules.py
    │           │   │   ├── cb_rules.pyi
    │           │   │   ├── cfuncs.py
    │           │   │   ├── cfuncs.pyi
    │           │   │   ├── common_rules.py
    │           │   │   ├── common_rules.pyi
    │           │   │   ├── crackfortran.py
    │           │   │   ├── crackfortran.pyi
    │           │   │   ├── diagnose.py
    │           │   │   ├── diagnose.pyi
    │           │   │   ├── f2py2e.py
    │           │   │   ├── f2py2e.pyi
    │           │   │   ├── f90mod_rules.py
    │           │   │   ├── f90mod_rules.pyi
    │           │   │   ├── func2subr.py
    │           │   │   ├── func2subr.pyi
    │           │   │   ├── rules.py
    │           │   │   ├── rules.pyi
    │           │   │   ├── setup.cfg
    │           │   │   ├── src
    │           │   │   │   ├── fortranobject.c
    │           │   │   │   └── fortranobject.h
    │           │   │   ├── symbolic.py
    │           │   │   ├── symbolic.pyi
    │           │   │   ├── tests
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── src
    │           │   │   │   │   ├── abstract_interface
    │           │   │   │   │   │   ├── foo.f90
    │           │   │   │   │   │   └── gh18403_mod.f90
    │           │   │   │   │   ├── array_from_pyobj
    │           │   │   │   │   │   └── wrapmodule.c
    │           │   │   │   │   ├── assumed_shape
    │           │   │   │   │   │   ├── .f2py_f2cmap
    │           │   │   │   │   │   ├── foo_free.f90
    │           │   │   │   │   │   ├── foo_mod.f90
    │           │   │   │   │   │   ├── foo_use.f90
    │           │   │   │   │   │   └── precision.f90
    │           │   │   │   │   ├── block_docstring
    │           │   │   │   │   │   └── foo.f
    │           │   │   │   │   ├── callback
    │           │   │   │   │   │   ├── foo.f
    │           │   │   │   │   │   ├── gh17797.f90
    │           │   │   │   │   │   ├── gh18335.f90
    │           │   │   │   │   │   ├── gh25211.f
    │           │   │   │   │   │   ├── gh25211.pyf
    │           │   │   │   │   │   └── gh26681.f90
    │           │   │   │   │   ├── cli
    │           │   │   │   │   │   ├── gh_22819.pyf
    │           │   │   │   │   │   ├── hi77.f
    │           │   │   │   │   │   └── hiworld.f90
    │           │   │   │   │   ├── common
    │           │   │   │   │   │   ├── block.f
    │           │   │   │   │   │   └── gh19161.f90
    │           │   │   │   │   ├── crackfortran
    │           │   │   │   │   │   ├── accesstype.f90
    │           │   │   │   │   │   ├── common_with_division.f
    │           │   │   │   │   │   ├── data_common.f
    │           │   │   │   │   │   ├── data_multiplier.f
    │           │   │   │   │   │   ├── data_stmts.f90
    │           │   │   │   │   │   ├── data_with_comments.f
    │           │   │   │   │   │   ├── foo_deps.f90
    │           │   │   │   │   │   ├── gh15035.f
    │           │   │   │   │   │   ├── gh17859.f
    │           │   │   │   │   │   ├── gh22648.pyf
    │           │   │   │   │   │   ├── gh23533.f
    │           │   │   │   │   │   ├── gh23598.f90
    │           │   │   │   │   │   ├── gh23598Warn.f90
    │           │   │   │   │   │   ├── gh23879.f90
    │           │   │   │   │   │   ├── gh27697.f90
    │           │   │   │   │   │   ├── gh2848.f90
    │           │   │   │   │   │   ├── operators.f90
    │           │   │   │   │   │   ├── privatemod.f90
    │           │   │   │   │   │   ├── publicmod.f90
    │           │   │   │   │   │   ├── pubprivmod.f90
    │           │   │   │   │   │   └── unicode_comment.f90
    │           │   │   │   │   ├── f2cmap
    │           │   │   │   │   │   ├── .f2py_f2cmap
    │           │   │   │   │   │   └── isoFortranEnvMap.f90
    │           │   │   │   │   ├── inplace
    │           │   │   │   │   │   └── foo.f
    │           │   │   │   │   ├── isocintrin
    │           │   │   │   │   │   └── isoCtests.f90
    │           │   │   │   │   ├── kind
    │           │   │   │   │   │   └── foo.f90
    │           │   │   │   │   ├── mixed
    │           │   │   │   │   │   ├── foo.f
    │           │   │   │   │   │   ├── foo_fixed.f90
    │           │   │   │   │   │   └── foo_free.f90
    │           │   │   │   │   ├── modules
    │           │   │   │   │   │   ├── gh25337
    │           │   │   │   │   │   │   ├── data.f90
    │           │   │   │   │   │   │   └── use_data.f90
    │           │   │   │   │   │   ├── gh26920
    │           │   │   │   │   │   │   ├── two_mods_with_no_public_entities.f90
    │           │   │   │   │   │   │   └── two_mods_with_one_public_routine.f90
    │           │   │   │   │   │   ├── module_data_docstring.f90
    │           │   │   │   │   │   └── use_modules.f90
    │           │   │   │   │   ├── negative_bounds
    │           │   │   │   │   │   └── issue_20853.f90
    │           │   │   │   │   ├── parameter
    │           │   │   │   │   │   ├── constant_array.f90
    │           │   │   │   │   │   ├── constant_both.f90
    │           │   │   │   │   │   ├── constant_compound.f90
    │           │   │   │   │   │   ├── constant_integer.f90
    │           │   │   │   │   │   ├── constant_non_compound.f90
    │           │   │   │   │   │   └── constant_real.f90
    │           │   │   │   │   ├── quoted_character
    │           │   │   │   │   │   └── foo.f
    │           │   │   │   │   ├── regression
    │           │   │   │   │   │   ├── AB.inc
    │           │   │   │   │   │   ├── assignOnlyModule.f90
    │           │   │   │   │   │   ├── complex_struct_compat.f90
    │           │   │   │   │   │   ├── complex_struct_compat.pyf
    │           │   │   │   │   │   ├── datonly.f90
    │           │   │   │   │   │   ├── f77comments.f
    │           │   │   │   │   │   ├── f77fixedform.f95
    │           │   │   │   │   │   ├── f90continuation.f90
    │           │   │   │   │   │   ├── incfile.f90
    │           │   │   │   │   │   ├── inout.f90
    │           │   │   │   │   │   ├── lower_f2py_fortran.f90
    │           │   │   │   │   │   └── mod_derived_types.f90
    │           │   │   │   │   ├── return_character
    │           │   │   │   │   │   ├── foo77.f
    │           │   │   │   │   │   └── foo90.f90
    │           │   │   │   │   ├── return_complex
    │           │   │   │   │   │   ├── foo77.f
    │           │   │   │   │   │   └── foo90.f90
    │           │   │   │   │   ├── return_integer
    │           │   │   │   │   │   ├── foo77.f
    │           │   │   │   │   │   └── foo90.f90
    │           │   │   │   │   ├── return_logical
    │           │   │   │   │   │   ├── foo77.f
    │           │   │   │   │   │   └── foo90.f90
    │           │   │   │   │   ├── return_real
    │           │   │   │   │   │   ├── foo77.f
    │           │   │   │   │   │   └── foo90.f90
    │           │   │   │   │   ├── routines
    │           │   │   │   │   │   ├── funcfortranname.f
    │           │   │   │   │   │   ├── funcfortranname.pyf
    │           │   │   │   │   │   ├── subrout.f
    │           │   │   │   │   │   └── subrout.pyf
    │           │   │   │   │   ├── size
    │           │   │   │   │   │   └── foo.f90
    │           │   │   │   │   ├── string
    │           │   │   │   │   │   ├── char.f90
    │           │   │   │   │   │   ├── fixed_string.f90
    │           │   │   │   │   │   ├── gh24008.f
    │           │   │   │   │   │   ├── gh24662.f90
    │           │   │   │   │   │   ├── gh25286.f90
    │           │   │   │   │   │   ├── gh25286.pyf
    │           │   │   │   │   │   ├── gh25286_bc.pyf
    │           │   │   │   │   │   ├── scalar_string.f90
    │           │   │   │   │   │   └── string.f
    │           │   │   │   │   └── value_attrspec
    │           │   │   │   │       └── gh21665.f90
    │           │   │   │   ├── test_abstract_interface.py
    │           │   │   │   ├── test_array_from_pyobj.py
    │           │   │   │   ├── test_assumed_shape.py
    │           │   │   │   ├── test_block_docstring.py
    │           │   │   │   ├── test_callback.py
    │           │   │   │   ├── test_capi_maps.py
    │           │   │   │   ├── test_character.py
    │           │   │   │   ├── test_common.py
    │           │   │   │   ├── test_crackfortran.py
    │           │   │   │   ├── test_data.py
    │           │   │   │   ├── test_docs.py
    │           │   │   │   ├── test_f2cmap.py
    │           │   │   │   ├── test_f2py2e.py
    │           │   │   │   ├── test_inplace.py
    │           │   │   │   ├── test_isoc.py
    │           │   │   │   ├── test_kind.py
    │           │   │   │   ├── test_mixed.py
    │           │   │   │   ├── test_modules.py
    │           │   │   │   ├── test_parameter.py
    │           │   │   │   ├── test_pyf_src.py
    │           │   │   │   ├── test_quoted_character.py
    │           │   │   │   ├── test_regression.py
    │           │   │   │   ├── test_return_character.py
    │           │   │   │   ├── test_return_complex.py
    │           │   │   │   ├── test_return_integer.py
    │           │   │   │   ├── test_return_logical.py
    │           │   │   │   ├── test_return_real.py
    │           │   │   │   ├── test_routines.py
    │           │   │   │   ├── test_semicolon_split.py
    │           │   │   │   ├── test_size.py
    │           │   │   │   ├── test_string.py
    │           │   │   │   ├── test_symbolic.py
    │           │   │   │   ├── test_value_attrspec.py
    │           │   │   │   └── util.py
    │           │   │   ├── use_rules.py
    │           │   │   └── use_rules.pyi
    │           │   ├── fft
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _helper.py
    │           │   │   ├── _helper.pyi
    │           │   │   ├── _pocketfft.py
    │           │   │   ├── _pocketfft.pyi
    │           │   │   ├── _pocketfft_umath.cpython-314-x86_64-linux-gnu.so
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── test_helper.py
    │           │   │       └── test_pocketfft.py
    │           │   ├── lib
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _array_utils_impl.py
    │           │   │   ├── _array_utils_impl.pyi
    │           │   │   ├── _arraypad_impl.py
    │           │   │   ├── _arraypad_impl.pyi
    │           │   │   ├── _arraysetops_impl.py
    │           │   │   ├── _arraysetops_impl.pyi
    │           │   │   ├── _arrayterator_impl.py
    │           │   │   ├── _arrayterator_impl.pyi
    │           │   │   ├── _datasource.py
    │           │   │   ├── _datasource.pyi
    │           │   │   ├── _format_impl.py
    │           │   │   ├── _format_impl.pyi
    │           │   │   ├── _function_base_impl.py
    │           │   │   ├── _function_base_impl.pyi
    │           │   │   ├── _histograms_impl.py
    │           │   │   ├── _histograms_impl.pyi
    │           │   │   ├── _index_tricks_impl.py
    │           │   │   ├── _index_tricks_impl.pyi
    │           │   │   ├── _iotools.py
    │           │   │   ├── _iotools.pyi
    │           │   │   ├── _nanfunctions_impl.py
    │           │   │   ├── _nanfunctions_impl.pyi
    │           │   │   ├── _npyio_impl.py
    │           │   │   ├── _npyio_impl.pyi
    │           │   │   ├── _polynomial_impl.py
    │           │   │   ├── _polynomial_impl.pyi
    │           │   │   ├── _scimath_impl.py
    │           │   │   ├── _scimath_impl.pyi
    │           │   │   ├── _shape_base_impl.py
    │           │   │   ├── _shape_base_impl.pyi
    │           │   │   ├── _stride_tricks_impl.py
    │           │   │   ├── _stride_tricks_impl.pyi
    │           │   │   ├── _twodim_base_impl.py
    │           │   │   ├── _twodim_base_impl.pyi
    │           │   │   ├── _type_check_impl.py
    │           │   │   ├── _type_check_impl.pyi
    │           │   │   ├── _ufunclike_impl.py
    │           │   │   ├── _ufunclike_impl.pyi
    │           │   │   ├── _user_array_impl.py
    │           │   │   ├── _user_array_impl.pyi
    │           │   │   ├── _utils_impl.py
    │           │   │   ├── _utils_impl.pyi
    │           │   │   ├── _version.py
    │           │   │   ├── _version.pyi
    │           │   │   ├── array_utils.py
    │           │   │   ├── array_utils.pyi
    │           │   │   ├── format.py
    │           │   │   ├── format.pyi
    │           │   │   ├── introspect.py
    │           │   │   ├── introspect.pyi
    │           │   │   ├── mixins.py
    │           │   │   ├── mixins.pyi
    │           │   │   ├── npyio.py
    │           │   │   ├── npyio.pyi
    │           │   │   ├── recfunctions.py
    │           │   │   ├── recfunctions.pyi
    │           │   │   ├── scimath.py
    │           │   │   ├── scimath.pyi
    │           │   │   ├── stride_tricks.py
    │           │   │   ├── stride_tricks.pyi
    │           │   │   ├── tests
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── data
    │           │   │   │   │   ├── py2-np0-objarr.npy
    │           │   │   │   │   ├── py2-objarr.npy
    │           │   │   │   │   ├── py2-objarr.npz
    │           │   │   │   │   ├── py3-objarr.npy
    │           │   │   │   │   ├── py3-objarr.npz
    │           │   │   │   │   ├── python3.npy
    │           │   │   │   │   └── win64python2.npy
    │           │   │   │   ├── test__datasource.py
    │           │   │   │   ├── test__iotools.py
    │           │   │   │   ├── test__version.py
    │           │   │   │   ├── test_array_utils.py
    │           │   │   │   ├── test_arraypad.py
    │           │   │   │   ├── test_arraysetops.py
    │           │   │   │   ├── test_arrayterator.py
    │           │   │   │   ├── test_format.py
    │           │   │   │   ├── test_function_base.py
    │           │   │   │   ├── test_histograms.py
    │           │   │   │   ├── test_index_tricks.py
    │           │   │   │   ├── test_io.py
    │           │   │   │   ├── test_loadtxt.py
    │           │   │   │   ├── test_mixins.py
    │           │   │   │   ├── test_nanfunctions.py
    │           │   │   │   ├── test_packbits.py
    │           │   │   │   ├── test_polynomial.py
    │           │   │   │   ├── test_recfunctions.py
    │           │   │   │   ├── test_regression.py
    │           │   │   │   ├── test_shape_base.py
    │           │   │   │   ├── test_stride_tricks.py
    │           │   │   │   ├── test_twodim_base.py
    │           │   │   │   ├── test_type_check.py
    │           │   │   │   ├── test_ufunclike.py
    │           │   │   │   └── test_utils.py
    │           │   │   ├── user_array.py
    │           │   │   └── user_array.pyi
    │           │   ├── linalg
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _linalg.py
    │           │   │   ├── _linalg.pyi
    │           │   │   ├── _umath_linalg.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _umath_linalg.pyi
    │           │   │   ├── lapack_lite.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── lapack_lite.pyi
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── test_deprecations.py
    │           │   │       ├── test_linalg.py
    │           │   │       └── test_regression.py
    │           │   ├── ma
    │           │   │   ├── API_CHANGES.txt
    │           │   │   ├── LICENSE
    │           │   │   ├── README.rst
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── core.py
    │           │   │   ├── core.pyi
    │           │   │   ├── extras.py
    │           │   │   ├── extras.pyi
    │           │   │   ├── mrecords.py
    │           │   │   ├── mrecords.pyi
    │           │   │   ├── tests
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_arrayobject.py
    │           │   │   │   ├── test_core.py
    │           │   │   │   ├── test_deprecations.py
    │           │   │   │   ├── test_extras.py
    │           │   │   │   ├── test_mrecords.py
    │           │   │   │   ├── test_old_ma.py
    │           │   │   │   ├── test_regression.py
    │           │   │   │   └── test_subclassing.py
    │           │   │   ├── testutils.py
    │           │   │   └── testutils.pyi
    │           │   ├── matlib.py
    │           │   ├── matlib.pyi
    │           │   ├── matrixlib
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── defmatrix.py
    │           │   │   ├── defmatrix.pyi
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── test_defmatrix.py
    │           │   │       ├── test_interaction.py
    │           │   │       ├── test_masked_matrix.py
    │           │   │       ├── test_matrix_linalg.py
    │           │   │       ├── test_multiarray.py
    │           │   │       ├── test_numeric.py
    │           │   │       └── test_regression.py
    │           │   ├── polynomial
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _polybase.py
    │           │   │   ├── _polybase.pyi
    │           │   │   ├── _polytypes.pyi
    │           │   │   ├── chebyshev.py
    │           │   │   ├── chebyshev.pyi
    │           │   │   ├── hermite.py
    │           │   │   ├── hermite.pyi
    │           │   │   ├── hermite_e.py
    │           │   │   ├── hermite_e.pyi
    │           │   │   ├── laguerre.py
    │           │   │   ├── laguerre.pyi
    │           │   │   ├── legendre.py
    │           │   │   ├── legendre.pyi
    │           │   │   ├── polynomial.py
    │           │   │   ├── polynomial.pyi
    │           │   │   ├── polyutils.py
    │           │   │   ├── polyutils.pyi
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── test_chebyshev.py
    │           │   │       ├── test_classes.py
    │           │   │       ├── test_hermite.py
    │           │   │       ├── test_hermite_e.py
    │           │   │       ├── test_laguerre.py
    │           │   │       ├── test_legendre.py
    │           │   │       ├── test_polynomial.py
    │           │   │       ├── test_polyutils.py
    │           │   │       ├── test_printing.py
    │           │   │       └── test_symbol.py
    │           │   ├── py.typed
    │           │   ├── random
    │           │   │   ├── LICENSE.md
    │           │   │   ├── __init__.pxd
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _bounded_integers.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _bounded_integers.pxd
    │           │   │   ├── _bounded_integers.pyi
    │           │   │   ├── _common.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _common.pxd
    │           │   │   ├── _common.pyi
    │           │   │   ├── _examples
    │           │   │   │   ├── cffi
    │           │   │   │   │   ├── extending.py
    │           │   │   │   │   └── parse.py
    │           │   │   │   ├── cython
    │           │   │   │   │   ├── extending.pyx
    │           │   │   │   │   ├── extending_distributions.pyx
    │           │   │   │   │   └── meson.build
    │           │   │   │   └── numba
    │           │   │   │       ├── extending.py
    │           │   │   │       └── extending_distributions.py
    │           │   │   ├── _generator.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _generator.pyi
    │           │   │   ├── _mt19937.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _mt19937.pyi
    │           │   │   ├── _pcg64.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _pcg64.pyi
    │           │   │   ├── _philox.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _philox.pyi
    │           │   │   ├── _pickle.py
    │           │   │   ├── _pickle.pyi
    │           │   │   ├── _sfc64.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _sfc64.pyi
    │           │   │   ├── bit_generator.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── bit_generator.pxd
    │           │   │   ├── bit_generator.pyi
    │           │   │   ├── c_distributions.pxd
    │           │   │   ├── lib
    │           │   │   │   └── libnpyrandom.a
    │           │   │   ├── mtrand.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── mtrand.pyi
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── data
    │           │   │       │   ├── __init__.py
    │           │   │       │   ├── generator_pcg64_np121.pkl.gz
    │           │   │       │   ├── generator_pcg64_np126.pkl.gz
    │           │   │       │   ├── mt19937-testset-1.csv
    │           │   │       │   ├── mt19937-testset-2.csv
    │           │   │       │   ├── pcg64-testset-1.csv
    │           │   │       │   ├── pcg64-testset-2.csv
    │           │   │       │   ├── pcg64dxsm-testset-1.csv
    │           │   │       │   ├── pcg64dxsm-testset-2.csv
    │           │   │       │   ├── philox-testset-1.csv
    │           │   │       │   ├── philox-testset-2.csv
    │           │   │       │   ├── sfc64-testset-1.csv
    │           │   │       │   ├── sfc64-testset-2.csv
    │           │   │       │   └── sfc64_np126.pkl.gz
    │           │   │       ├── test_direct.py
    │           │   │       ├── test_extending.py
    │           │   │       ├── test_generator_mt19937.py
    │           │   │       ├── test_generator_mt19937_regressions.py
    │           │   │       ├── test_random.py
    │           │   │       ├── test_randomstate.py
    │           │   │       ├── test_randomstate_regression.py
    │           │   │       ├── test_regression.py
    │           │   │       ├── test_seed_sequence.py
    │           │   │       └── test_smoke.py
    │           │   ├── rec
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── strings
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── testing
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── _private
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __init__.pyi
    │           │   │   │   ├── extbuild.py
    │           │   │   │   ├── extbuild.pyi
    │           │   │   │   ├── utils.py
    │           │   │   │   └── utils.pyi
    │           │   │   ├── overrides.py
    │           │   │   ├── overrides.pyi
    │           │   │   ├── print_coercion_tables.py
    │           │   │   ├── print_coercion_tables.pyi
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       └── test_utils.py
    │           │   ├── tests
    │           │   │   ├── __init__.py
    │           │   │   ├── test__all__.py
    │           │   │   ├── test_configtool.py
    │           │   │   ├── test_ctypeslib.py
    │           │   │   ├── test_lazyloading.py
    │           │   │   ├── test_matlib.py
    │           │   │   ├── test_numpy_config.py
    │           │   │   ├── test_numpy_version.py
    │           │   │   ├── test_public_api.py
    │           │   │   ├── test_reloading.py
    │           │   │   ├── test_scripts.py
    │           │   │   └── test_warnings.py
    │           │   ├── typing
    │           │   │   ├── __init__.py
    │           │   │   ├── __init__.pyi
    │           │   │   ├── mypy_plugin.py
    │           │   │   └── tests
    │           │   │       ├── __init__.py
    │           │   │       ├── data
    │           │   │       │   ├── fail
    │           │   │       │   │   ├── arithmetic.pyi
    │           │   │       │   │   ├── array_constructors.pyi
    │           │   │       │   │   ├── array_like.pyi
    │           │   │       │   │   ├── array_pad.pyi
    │           │   │       │   │   ├── arrayprint.pyi
    │           │   │       │   │   ├── arrayterator.pyi
    │           │   │       │   │   ├── bitwise_ops.pyi
    │           │   │       │   │   ├── char.pyi
    │           │   │       │   │   ├── chararray.pyi
    │           │   │       │   │   ├── comparisons.pyi
    │           │   │       │   │   ├── constants.pyi
    │           │   │       │   │   ├── datasource.pyi
    │           │   │       │   │   ├── dtype.pyi
    │           │   │       │   │   ├── einsumfunc.pyi
    │           │   │       │   │   ├── flatiter.pyi
    │           │   │       │   │   ├── fromnumeric.pyi
    │           │   │       │   │   ├── histograms.pyi
    │           │   │       │   │   ├── index_tricks.pyi
    │           │   │       │   │   ├── lib_function_base.pyi
    │           │   │       │   │   ├── lib_polynomial.pyi
    │           │   │       │   │   ├── lib_utils.pyi
    │           │   │       │   │   ├── lib_version.pyi
    │           │   │       │   │   ├── linalg.pyi
    │           │   │       │   │   ├── ma.pyi
    │           │   │       │   │   ├── memmap.pyi
    │           │   │       │   │   ├── modules.pyi
    │           │   │       │   │   ├── multiarray.pyi
    │           │   │       │   │   ├── ndarray.pyi
    │           │   │       │   │   ├── ndarray_misc.pyi
    │           │   │       │   │   ├── nditer.pyi
    │           │   │       │   │   ├── nested_sequence.pyi
    │           │   │       │   │   ├── npyio.pyi
    │           │   │       │   │   ├── numerictypes.pyi
    │           │   │       │   │   ├── random.pyi
    │           │   │       │   │   ├── rec.pyi
    │           │   │       │   │   ├── scalars.pyi
    │           │   │       │   │   ├── shape.pyi
    │           │   │       │   │   ├── shape_base.pyi
    │           │   │       │   │   ├── stride_tricks.pyi
    │           │   │       │   │   ├── strings.pyi
    │           │   │       │   │   ├── testing.pyi
    │           │   │       │   │   ├── twodim_base.pyi
    │           │   │       │   │   ├── type_check.pyi
    │           │   │       │   │   ├── ufunc_config.pyi
    │           │   │       │   │   ├── ufunclike.pyi
    │           │   │       │   │   ├── ufuncs.pyi
    │           │   │       │   │   └── warnings_and_errors.pyi
    │           │   │       │   ├── misc
    │           │   │       │   │   └── extended_precision.pyi
    │           │   │       │   ├── mypy.ini
    │           │   │       │   ├── pass
    │           │   │       │   │   ├── arithmetic.py
    │           │   │       │   │   ├── array_constructors.py
    │           │   │       │   │   ├── array_like.py
    │           │   │       │   │   ├── arrayprint.py
    │           │   │       │   │   ├── arrayterator.py
    │           │   │       │   │   ├── bitwise_ops.py
    │           │   │       │   │   ├── comparisons.py
    │           │   │       │   │   ├── dtype.py
    │           │   │       │   │   ├── einsumfunc.py
    │           │   │       │   │   ├── flatiter.py
    │           │   │       │   │   ├── fromnumeric.py
    │           │   │       │   │   ├── index_tricks.py
    │           │   │       │   │   ├── lib_user_array.py
    │           │   │       │   │   ├── lib_utils.py
    │           │   │       │   │   ├── lib_version.py
    │           │   │       │   │   ├── literal.py
    │           │   │       │   │   ├── ma.py
    │           │   │       │   │   ├── mod.py
    │           │   │       │   │   ├── modules.py
    │           │   │       │   │   ├── multiarray.py
    │           │   │       │   │   ├── ndarray_conversion.py
    │           │   │       │   │   ├── ndarray_misc.py
    │           │   │       │   │   ├── ndarray_shape_manipulation.py
    │           │   │       │   │   ├── nditer.py
    │           │   │       │   │   ├── numeric.py
    │           │   │       │   │   ├── numerictypes.py
    │           │   │       │   │   ├── random.py
    │           │   │       │   │   ├── recfunctions.py
    │           │   │       │   │   ├── scalars.py
    │           │   │       │   │   ├── shape.py
    │           │   │       │   │   ├── simple.py
    │           │   │       │   │   ├── ufunc_config.py
    │           │   │       │   │   ├── ufunclike.py
    │           │   │       │   │   ├── ufuncs.py
    │           │   │       │   │   └── warnings_and_errors.py
    │           │   │       │   └── reveal
    │           │   │       │       ├── arithmetic.pyi
    │           │   │       │       ├── array_api_info.pyi
    │           │   │       │       ├── array_constructors.pyi
    │           │   │       │       ├── arraypad.pyi
    │           │   │       │       ├── arrayprint.pyi
    │           │   │       │       ├── arraysetops.pyi
    │           │   │       │       ├── arrayterator.pyi
    │           │   │       │       ├── bitwise_ops.pyi
    │           │   │       │       ├── char.pyi
    │           │   │       │       ├── chararray.pyi
    │           │   │       │       ├── comparisons.pyi
    │           │   │       │       ├── constants.pyi
    │           │   │       │       ├── ctypeslib.pyi
    │           │   │       │       ├── datasource.pyi
    │           │   │       │       ├── dtype.pyi
    │           │   │       │       ├── einsumfunc.pyi
    │           │   │       │       ├── emath.pyi
    │           │   │       │       ├── fft.pyi
    │           │   │       │       ├── flatiter.pyi
    │           │   │       │       ├── fromnumeric.pyi
    │           │   │       │       ├── getlimits.pyi
    │           │   │       │       ├── histograms.pyi
    │           │   │       │       ├── index_tricks.pyi
    │           │   │       │       ├── lib_function_base.pyi
    │           │   │       │       ├── lib_polynomial.pyi
    │           │   │       │       ├── lib_utils.pyi
    │           │   │       │       ├── lib_version.pyi
    │           │   │       │       ├── linalg.pyi
    │           │   │       │       ├── ma.pyi
    │           │   │       │       ├── matrix.pyi
    │           │   │       │       ├── memmap.pyi
    │           │   │       │       ├── mod.pyi
    │           │   │       │       ├── modules.pyi
    │           │   │       │       ├── multiarray.pyi
    │           │   │       │       ├── nbit_base_example.pyi
    │           │   │       │       ├── ndarray_assignability.pyi
    │           │   │       │       ├── ndarray_conversion.pyi
    │           │   │       │       ├── ndarray_misc.pyi
    │           │   │       │       ├── ndarray_shape_manipulation.pyi
    │           │   │       │       ├── nditer.pyi
    │           │   │       │       ├── nested_sequence.pyi
    │           │   │       │       ├── npyio.pyi
    │           │   │       │       ├── numeric.pyi
    │           │   │       │       ├── numerictypes.pyi
    │           │   │       │       ├── polynomial_polybase.pyi
    │           │   │       │       ├── polynomial_polyutils.pyi
    │           │   │       │       ├── polynomial_series.pyi
    │           │   │       │       ├── random.pyi
    │           │   │       │       ├── rec.pyi
    │           │   │       │       ├── scalars.pyi
    │           │   │       │       ├── shape.pyi
    │           │   │       │       ├── shape_base.pyi
    │           │   │       │       ├── stride_tricks.pyi
    │           │   │       │       ├── strings.pyi
    │           │   │       │       ├── testing.pyi
    │           │   │       │       ├── twodim_base.pyi
    │           │   │       │       ├── type_check.pyi
    │           │   │       │       ├── ufunc_config.pyi
    │           │   │       │       ├── ufunclike.pyi
    │           │   │       │       ├── ufuncs.pyi
    │           │   │       │       └── warnings_and_errors.pyi
    │           │   │       ├── test_isfile.py
    │           │   │       ├── test_runtime.py
    │           │   │       └── test_typing.py
    │           │   ├── version.py
    │           │   └── version.pyi
    │           ├── numpy-2.5.4.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       ├── LICENSE.txt
    │           │       └── numpy
    │           │           ├── _core
    │           │           │   ├── include
    │           │           │   │   └── numpy
    │           │           │   │       └── libdivide
    │           │           │   │           └── LICENSE.txt
    │           │           │   └── src
    │           │           │       ├── common
    │           │           │       │   └── pythoncapi-compat
    │           │           │       │       └── COPYING
    │           │           │       ├── highway
    │           │           │       │   └── LICENSE
    │           │           │       ├── multiarray
    │           │           │       │   └── dragon4_LICENSE.txt
    │           │           │       ├── npysort
    │           │           │       │   └── x86-simd-sort
    │           │           │       │       └── LICENSE.md
    │           │           │       └── umath
    │           │           │           └── svml
    │           │           │               └── LICENSE
    │           │           ├── fft
    │           │           │   └── pocketfft
    │           │           │       └── LICENSE.md
    │           │           ├── linalg
    │           │           │   └── lapack_lite
    │           │           │       └── LICENSE.txt
    │           │           ├── ma
    │           │           │   └── LICENSE
    │           │           └── random
    │           │               ├── LICENSE.md
    │           │               └── src
    │           │                   ├── distributions
    │           │                   │   └── LICENSE.md
    │           │                   ├── mt19937
    │           │                   │   └── LICENSE.md
    │           │                   ├── pcg64
    │           │                   │   └── LICENSE.md
    │           │                   ├── philox
    │           │                   │   └── LICENSE.md
    │           │                   ├── sfc64
    │           │                   │   └── LICENSE.md
    │           │                   └── splitmix64
    │           │                       └── LICENSE.md
    │           ├── numpy.libs
    │           │   ├── libgfortran-83c28eba-468e71e5.so.5.0.0
    │           │   ├── libquadmath-2284e583-a9307bba.so.0.0.0
    │           │   └── libscipy_openblas64_-f48b354e.so
    │           ├── onnxruntime
    │           │   ├── LICENSE
    │           │   ├── Privacy.md
    │           │   ├── ThirdPartyNotices.txt
    │           │   ├── __init__.py
    │           │   ├── backend
    │           │   │   ├── __init__.py
    │           │   │   ├── backend.py
    │           │   │   └── backend_rep.py
    │           │   ├── capi
    │           │   │   ├── __init__.py
    │           │   │   ├── _ld_preload.py
    │           │   │   ├── _pybind_state.py
    │           │   │   ├── build_and_package_info.py
    │           │   │   ├── convert_npz_to_onnx_adapter.py
    │           │   │   ├── libonnxruntime.so.1.32.0
    │           │   │   ├── libonnxruntime_providers_shared.so
    │           │   │   ├── onnxruntime_collect_build_info.py
    │           │   │   ├── onnxruntime_inference_collection.py
    │           │   │   ├── onnxruntime_pybind11_state.cpython-314-x86_64-linux-gnu.so
    │           │   │   └── onnxruntime_validation.py
    │           │   ├── datasets
    │           │   │   ├── __init__.py
    │           │   │   ├── logreg_iris.onnx
    │           │   │   ├── mul_1.onnx
    │           │   │   └── sigmoid.onnx
    │           │   ├── quantization
    │           │   │   ├── CalTableFlatBuffers
    │           │   │   │   ├── KeyValue.py
    │           │   │   │   ├── TrtTable.py
    │           │   │   │   └── __init__.py
    │           │   │   ├── __init__.py
    │           │   │   ├── base_quantizer.py
    │           │   │   ├── calibrate.py
    │           │   │   ├── cuda_quantizer.py
    │           │   │   ├── execution_providers
    │           │   │   │   └── qnn
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── fusion_lpnorm.py
    │           │   │   │       ├── fusion_spacetodepth.py
    │           │   │   │       ├── mixed_precision_overrides_utils.py
    │           │   │   │       ├── preprocess.py
    │           │   │   │       └── quant_config.py
    │           │   │   ├── fusions
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── fusion.py
    │           │   │   │   ├── fusion_gelu.py
    │           │   │   │   ├── fusion_layernorm.py
    │           │   │   │   └── replace_upsample_with_resize.py
    │           │   │   ├── matmul_bnb4_quantizer.py
    │           │   │   ├── matmul_nbits_quantizer.py
    │           │   │   ├── neural_compressor
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── onnx_model.py
    │           │   │   │   ├── util.py
    │           │   │   │   └── weight_only.py
    │           │   │   ├── onnx_model.py
    │           │   │   ├── onnx_quantizer.py
    │           │   │   ├── operators
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── activation.py
    │           │   │   │   ├── argmax.py
    │           │   │   │   ├── attention.py
    │           │   │   │   ├── base_operator.py
    │           │   │   │   ├── binary_op.py
    │           │   │   │   ├── concat.py
    │           │   │   │   ├── conv.py
    │           │   │   │   ├── direct_q8.py
    │           │   │   │   ├── embed_layernorm.py
    │           │   │   │   ├── gather.py
    │           │   │   │   ├── gavgpool.py
    │           │   │   │   ├── gemm.py
    │           │   │   │   ├── lstm.py
    │           │   │   │   ├── matmul.py
    │           │   │   │   ├── maxpool.py
    │           │   │   │   ├── norm.py
    │           │   │   │   ├── pad.py
    │           │   │   │   ├── pooling.py
    │           │   │   │   ├── qdq_base_operator.py
    │           │   │   │   ├── resize.py
    │           │   │   │   ├── softmax.py
    │           │   │   │   ├── split.py
    │           │   │   │   └── where.py
    │           │   │   ├── preprocess.py
    │           │   │   ├── qdq_loss_debug.py
    │           │   │   ├── qdq_quantizer.py
    │           │   │   ├── quant_utils.py
    │           │   │   ├── quantize.py
    │           │   │   ├── registry.py
    │           │   │   ├── shape_inference.py
    │           │   │   ├── static_quantize_runner.py
    │           │   │   └── tensor_quant_overrides.py
    │           │   ├── tools
    │           │   │   ├── __init__.py
    │           │   │   ├── check_onnx_model_mobile_usability.py
    │           │   │   ├── convert_onnx_models_to_ort.py
    │           │   │   ├── file_utils.py
    │           │   │   ├── fpa_intb_tune.py
    │           │   │   ├── logger.py
    │           │   │   ├── make_dynamic_shape_fixed.py
    │           │   │   ├── mobile_helpers
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── coreml_supported_mlprogram_ops.md
    │           │   │   │   ├── coreml_supported_neuralnetwork_ops.md
    │           │   │   │   ├── nnapi_supported_ops.md
    │           │   │   │   └── usability_checker.py
    │           │   │   ├── offline_tuning.py
    │           │   │   ├── onnx_model_utils.py
    │           │   │   ├── onnx_randomizer.py
    │           │   │   ├── onnxruntime_test.py
    │           │   │   ├── optimize_onnx_model.py
    │           │   │   ├── ort_format_model
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── operator_type_usage_processors.py
    │           │   │   │   ├── ort_flatbuffers_py
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── fbs
    │           │   │   │   │       ├── ArgType.py
    │           │   │   │   │       ├── ArgTypeAndIndex.py
    │           │   │   │   │       ├── Attribute.py
    │           │   │   │   │       ├── AttributeType.py
    │           │   │   │   │       ├── Checkpoint.py
    │           │   │   │   │       ├── DeprecatedKernelCreateInfos.py
    │           │   │   │   │       ├── DeprecatedNodeIndexAndKernelDefHash.py
    │           │   │   │   │       ├── DeprecatedSessionState.py
    │           │   │   │   │       ├── DeprecatedSubGraphSessionState.py
    │           │   │   │   │       ├── Dimension.py
    │           │   │   │   │       ├── DimensionValue.py
    │           │   │   │   │       ├── DimensionValueType.py
    │           │   │   │   │       ├── EdgeEnd.py
    │           │   │   │   │       ├── FloatProperty.py
    │           │   │   │   │       ├── Graph.py
    │           │   │   │   │       ├── InferenceSession.py
    │           │   │   │   │       ├── IntProperty.py
    │           │   │   │   │       ├── KernelTypeStrArgsEntry.py
    │           │   │   │   │       ├── KernelTypeStrResolver.py
    │           │   │   │   │       ├── MapType.py
    │           │   │   │   │       ├── Model.py
    │           │   │   │   │       ├── ModuleState.py
    │           │   │   │   │       ├── Node.py
    │           │   │   │   │       ├── NodeEdge.py
    │           │   │   │   │       ├── NodeType.py
    │           │   │   │   │       ├── NodesToOptimizeIndices.py
    │           │   │   │   │       ├── OpIdKernelTypeStrArgsEntry.py
    │           │   │   │   │       ├── OperatorSetId.py
    │           │   │   │   │       ├── OptimizerGroup.py
    │           │   │   │   │       ├── ParameterOptimizerState.py
    │           │   │   │   │       ├── PropertyBag.py
    │           │   │   │   │       ├── RuntimeOptimizationRecord.py
    │           │   │   │   │       ├── RuntimeOptimizationRecordContainerEntry.py
    │           │   │   │   │       ├── RuntimeOptimizations.py
    │           │   │   │   │       ├── SequenceType.py
    │           │   │   │   │       ├── Shape.py
    │           │   │   │   │       ├── SparseTensor.py
    │           │   │   │   │       ├── StringProperty.py
    │           │   │   │   │       ├── StringStringEntry.py
    │           │   │   │   │       ├── Tensor.py
    │           │   │   │   │       ├── TensorDataType.py
    │           │   │   │   │       ├── TensorTypeAndShape.py
    │           │   │   │   │       ├── TypeInfo.py
    │           │   │   │   │       ├── TypeInfoValue.py
    │           │   │   │   │       ├── ValueInfo.py
    │           │   │   │   │       └── __init__.py
    │           │   │   │   ├── ort_model_processor.py
    │           │   │   │   ├── types.py
    │           │   │   │   └── utils.py
    │           │   │   ├── pytorch_export_contrib_ops.py
    │           │   │   ├── pytorch_export_helpers.py
    │           │   │   ├── qdq_helpers
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── optimize_qdq_model.py
    │           │   │   ├── qnn
    │           │   │   │   ├── add_trans_cast.py
    │           │   │   │   ├── gen_qnn_ctx_onnx_model.py
    │           │   │   │   └── preprocess.py
    │           │   │   ├── reduced_build_config_parser.py
    │           │   │   ├── remove_initializer_from_input.py
    │           │   │   ├── symbolic_shape_infer.py
    │           │   │   └── update_onnx_opset.py
    │           │   └── transformers
    │           │       ├── __init__.py
    │           │       ├── affinity_helper.py
    │           │       ├── benchmark.py
    │           │       ├── benchmark_helper.py
    │           │       ├── bert_perf_test.py
    │           │       ├── bert_test_data.py
    │           │       ├── compare_bert_results.py
    │           │       ├── constants.py
    │           │       ├── convert_generation.py
    │           │       ├── convert_tf_models_to_pytorch.py
    │           │       ├── convert_to_packing_mode.py
    │           │       ├── dynamo_onnx_helper.py
    │           │       ├── float16.py
    │           │       ├── fusion_attention.py
    │           │       ├── fusion_attention_clip.py
    │           │       ├── fusion_attention_sam2.py
    │           │       ├── fusion_attention_unet.py
    │           │       ├── fusion_attention_vae.py
    │           │       ├── fusion_bart_attention.py
    │           │       ├── fusion_base.py
    │           │       ├── fusion_bias_add.py
    │           │       ├── fusion_biasgelu.py
    │           │       ├── fusion_biassplitgelu.py
    │           │       ├── fusion_conformer_attention.py
    │           │       ├── fusion_constant_fold.py
    │           │       ├── fusion_embedlayer.py
    │           │       ├── fusion_fastgelu.py
    │           │       ├── fusion_gelu.py
    │           │       ├── fusion_gelu_approximation.py
    │           │       ├── fusion_gemmfastgelu.py
    │           │       ├── fusion_gpt_attention.py
    │           │       ├── fusion_gpt_attention_megatron.py
    │           │       ├── fusion_gpt_attention_no_past.py
    │           │       ├── fusion_group_norm.py
    │           │       ├── fusion_layernorm.py
    │           │       ├── fusion_mha_dit.py
    │           │       ├── fusion_mha_mmdit.py
    │           │       ├── fusion_nhwc_conv.py
    │           │       ├── fusion_options.py
    │           │       ├── fusion_qordered_attention.py
    │           │       ├── fusion_qordered_gelu.py
    │           │       ├── fusion_qordered_layernorm.py
    │           │       ├── fusion_qordered_matmul.py
    │           │       ├── fusion_quickgelu.py
    │           │       ├── fusion_reshape.py
    │           │       ├── fusion_rotary_attention.py
    │           │       ├── fusion_shape.py
    │           │       ├── fusion_simplified_layernorm.py
    │           │       ├── fusion_skip_group_norm.py
    │           │       ├── fusion_skiplayernorm.py
    │           │       ├── fusion_transpose.py
    │           │       ├── fusion_utils.py
    │           │       ├── huggingface_models.py
    │           │       ├── import_utils.py
    │           │       ├── io_binding_helper.py
    │           │       ├── large_model_exporter.py
    │           │       ├── machine_info.py
    │           │       ├── metrics.py
    │           │       ├── models
    │           │       │   ├── bart
    │           │       │   │   ├── __init__.py
    │           │       │   │   └── export.py
    │           │       │   ├── bert
    │           │       │   │   ├── __init__.py
    │           │       │   │   └── eval_squad.py
    │           │       │   ├── gpt2
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── benchmark_gpt2.py
    │           │       │   │   ├── convert_to_onnx.py
    │           │       │   │   ├── gpt2_helper.py
    │           │       │   │   ├── gpt2_parity.py
    │           │       │   │   ├── gpt2_tester.py
    │           │       │   │   └── parity_check_helper.py
    │           │       │   ├── llama
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── benchmark.py
    │           │       │   │   ├── benchmark_all.py
    │           │       │   │   ├── benchmark_e2e.py
    │           │       │   │   ├── convert_to_onnx.py
    │           │       │   │   ├── dist_settings.py
    │           │       │   │   ├── llama_inputs.py
    │           │       │   │   ├── llama_parity.py
    │           │       │   │   ├── llama_torch.py
    │           │       │   │   └── quant_kv_dataloader.py
    │           │       │   ├── longformer
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── benchmark_longformer.py
    │           │       │   │   ├── convert_to_onnx.py
    │           │       │   │   ├── generate_test_data.py
    │           │       │   │   └── longformer_helper.py
    │           │       │   ├── phi2
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── convert_to_onnx.py
    │           │       │   │   └── inference_example.py
    │           │       │   ├── sam2
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── benchmark_sam2.py
    │           │       │   │   ├── convert_to_onnx.py
    │           │       │   │   ├── image_decoder.py
    │           │       │   │   ├── image_encoder.py
    │           │       │   │   ├── mask_decoder.py
    │           │       │   │   ├── nvtx_helper.py
    │           │       │   │   ├── prompt_encoder.py
    │           │       │   │   ├── sam2_demo.py
    │           │       │   │   ├── sam2_image_onnx_predictor.py
    │           │       │   │   └── sam2_utils.py
    │           │       │   ├── stable_diffusion
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── benchmark.py
    │           │       │   │   ├── benchmark_controlnet.py
    │           │       │   │   ├── demo_txt2img.py
    │           │       │   │   ├── demo_txt2img_xl.py
    │           │       │   │   ├── demo_utils.py
    │           │       │   │   ├── diffusion_models.py
    │           │       │   │   ├── diffusion_schedulers.py
    │           │       │   │   ├── engine_builder.py
    │           │       │   │   ├── engine_builder_ort_cuda.py
    │           │       │   │   ├── engine_builder_ort_trt.py
    │           │       │   │   ├── engine_builder_tensorrt.py
    │           │       │   │   ├── engine_builder_torch.py
    │           │       │   │   ├── optimize_pipeline.py
    │           │       │   │   ├── ort_optimizer.py
    │           │       │   │   ├── pipeline_stable_diffusion.py
    │           │       │   │   └── trt_utilities.py
    │           │       │   ├── t5
    │           │       │   │   ├── __init__.py
    │           │       │   │   ├── convert_to_onnx.py
    │           │       │   │   ├── t5_decoder.py
    │           │       │   │   ├── t5_encoder.py
    │           │       │   │   ├── t5_encoder_decoder_init.py
    │           │       │   │   └── t5_helper.py
    │           │       │   └── whisper
    │           │       │       ├── __init__.py
    │           │       │       ├── benchmark.py
    │           │       │       ├── benchmark_all.py
    │           │       │       ├── convert_to_onnx.py
    │           │       │       ├── whisper_chain.py
    │           │       │       ├── whisper_decoder.py
    │           │       │       ├── whisper_encoder.py
    │           │       │       ├── whisper_encoder_decoder_init.py
    │           │       │       ├── whisper_helper.py
    │           │       │       ├── whisper_inputs.py
    │           │       │       └── whisper_jump_times.py
    │           │       ├── onnx_exporter.py
    │           │       ├── onnx_model.py
    │           │       ├── onnx_model_bart.py
    │           │       ├── onnx_model_bert.py
    │           │       ├── onnx_model_bert_keras.py
    │           │       ├── onnx_model_bert_tf.py
    │           │       ├── onnx_model_clip.py
    │           │       ├── onnx_model_conformer.py
    │           │       ├── onnx_model_gpt2.py
    │           │       ├── onnx_model_mmdit.py
    │           │       ├── onnx_model_phi.py
    │           │       ├── onnx_model_sam2.py
    │           │       ├── onnx_model_t5.py
    │           │       ├── onnx_model_tnlr.py
    │           │       ├── onnx_model_unet.py
    │           │       ├── onnx_model_vae.py
    │           │       ├── onnx_utils.py
    │           │       ├── optimizer.py
    │           │       ├── past_helper.py
    │           │       ├── profile_result_processor.py
    │           │       ├── profiler.py
    │           │       ├── quantize_helper.py
    │           │       ├── shape_infer_helper.py
    │           │       ├── shape_optimizer.py
    │           │       └── torch_onnx_export_helper.py
    │           ├── onnxruntime-1.32.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── top_level.txt
    │           ├── openai
    │           │   ├── __init__.py
    │           │   ├── _base_client.py
    │           │   ├── _client.py
    │           │   ├── _compat.py
    │           │   ├── _constants.py
    │           │   ├── _data_residency.py
    │           │   ├── _event_handler.py
    │           │   ├── _exceptions.py
    │           │   ├── _extras
    │           │   │   ├── __init__.py
    │           │   │   ├── _common.py
    │           │   │   ├── numpy_proxy.py
    │           │   │   ├── pandas_proxy.py
    │           │   │   └── sounddevice_proxy.py
    │           │   ├── _files.py
    │           │   ├── _httpx2.py
    │           │   ├── _legacy_response.py
    │           │   ├── _models.py
    │           │   ├── _module_client.py
    │           │   ├── _multipart.py
    │           │   ├── _provider.py
    │           │   ├── _qs.py
    │           │   ├── _resource.py
    │           │   ├── _response.py
    │           │   ├── _send_queue.py
    │           │   ├── _streaming.py
    │           │   ├── _streaming_cleanup.py
    │           │   ├── _types.py
    │           │   ├── _utils
    │           │   │   ├── __init__.py
    │           │   │   ├── _compat.py
    │           │   │   ├── _datetime_parse.py
    │           │   │   ├── _json.py
    │           │   │   ├── _logs.py
    │           │   │   ├── _path.py
    │           │   │   ├── _proxy.py
    │           │   │   ├── _reflection.py
    │           │   │   ├── _resources_proxy.py
    │           │   │   ├── _streams.py
    │           │   │   ├── _sync.py
    │           │   │   ├── _transform.py
    │           │   │   ├── _typing.py
    │           │   │   └── _utils.py
    │           │   ├── _vendor
    │           │   │   ├── __init__.py
    │           │   │   └── httpx_aiohttp
    │           │   │       ├── FORK.md
    │           │   │       ├── LICENSE
    │           │   │       ├── README.md
    │           │   │       ├── __init__.py
    │           │   │       ├── client.py
    │           │   │       └── transport.py
    │           │   ├── _version.py
    │           │   ├── _websocket_connection.py
    │           │   ├── auth
    │           │   │   ├── __init__.py
    │           │   │   ├── _workload.py
    │           │   │   └── _x509.py
    │           │   ├── helpers
    │           │   │   ├── __init__.py
    │           │   │   ├── local_audio_player.py
    │           │   │   └── microphone.py
    │           │   ├── lib
    │           │   │   ├── .keep
    │           │   │   ├── __init__.py
    │           │   │   ├── _assistants_runs.py
    │           │   │   ├── _assistants_threads.py
    │           │   │   ├── _azure_websocket.py
    │           │   │   ├── _bedrock_auth.py
    │           │   │   ├── _chat_completion_resources.py
    │           │   │   ├── _client_auth.py
    │           │   │   ├── _files.py
    │           │   │   ├── _module_runtime.py
    │           │   │   ├── _old_api.py
    │           │   │   ├── _parsing
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _audio.py
    │           │   │   │   ├── _completions.py
    │           │   │   │   ├── _embeddings.py
    │           │   │   │   └── _responses.py
    │           │   │   ├── _pydantic.py
    │           │   │   ├── _realtime.py
    │           │   │   ├── _request_context.py
    │           │   │   ├── _response_resources.py
    │           │   │   ├── _tool_lifecycle.py
    │           │   │   ├── _tools.py
    │           │   │   ├── _uploads.py
    │           │   │   ├── _vector_stores.py
    │           │   │   ├── _webhooks.py
    │           │   │   ├── _websocket.py
    │           │   │   ├── azure.py
    │           │   │   ├── bedrock.py
    │           │   │   ├── beta
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── agents
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── _artifacts.py
    │           │   │   │       ├── _create.py
    │           │   │   │       ├── _files.py
    │           │   │   │       ├── _output.py
    │           │   │   │       ├── _result.py
    │           │   │   │       ├── _schema.py
    │           │   │   │       ├── _stream.py
    │           │   │   │       ├── _tool_error.py
    │           │   │   │       └── _tools.py
    │           │   │   ├── browser.py
    │           │   │   ├── computer.py
    │           │   │   ├── decisions_tool_runner.py
    │           │   │   ├── live
    │           │   │   │   ├── README.md
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _listeners.py
    │           │   │   │   ├── _transcript_grouper.py
    │           │   │   │   ├── _transcript_grouping.py
    │           │   │   │   ├── _transcript_state.py
    │           │   │   │   └── _types.py
    │           │   │   ├── realtime_translation.py
    │           │   │   ├── responses_tool_runner.py
    │           │   │   ├── responses_websocket
    │           │   │   │   ├── README.md
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _accumulator.py
    │           │   │   │   └── _session.py
    │           │   │   ├── streaming
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _assistants.py
    │           │   │   │   ├── _deltas.py
    │           │   │   │   ├── agents
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── _dispatch.py
    │           │   │   │   │   ├── _streams.py
    │           │   │   │   │   ├── _tools.py
    │           │   │   │   │   └── _types.py
    │           │   │   │   ├── chat
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── _completions.py
    │           │   │   │   │   ├── _events.py
    │           │   │   │   │   └── _types.py
    │           │   │   │   └── responses
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── _events.py
    │           │   │   │       ├── _responses.py
    │           │   │   │       └── _types.py
    │           │   │   └── tool_diagnostics.py
    │           │   ├── pagination.py
    │           │   ├── providers
    │           │   │   ├── __init__.py
    │           │   │   ├── bedrock.py
    │           │   │   └── vertex.py
    │           │   ├── py.typed
    │           │   ├── resources
    │           │   │   ├── __init__.py
    │           │   │   ├── admin
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── admin.py
    │           │   │   │   └── organization
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── admin_api_keys.py
    │           │   │   │       ├── audit_logs.py
    │           │   │   │       ├── certificates.py
    │           │   │   │       ├── data_retention.py
    │           │   │   │       ├── external_keys.py
    │           │   │   │       ├── external_storage.py
    │           │   │   │       ├── groups
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── groups.py
    │           │   │   │       │   ├── roles.py
    │           │   │   │       │   └── users.py
    │           │   │   │       ├── invites.py
    │           │   │   │       ├── organization.py
    │           │   │   │       ├── projects
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── api_keys.py
    │           │   │   │       │   ├── certificates.py
    │           │   │   │       │   ├── data_retention.py
    │           │   │   │       │   ├── groups
    │           │   │   │       │   │   ├── __init__.py
    │           │   │   │       │   │   ├── groups.py
    │           │   │   │       │   │   └── roles.py
    │           │   │   │       │   ├── hosted_tool_permissions.py
    │           │   │   │       │   ├── model_permissions.py
    │           │   │   │       │   ├── projects.py
    │           │   │   │       │   ├── rate_limits.py
    │           │   │   │       │   ├── roles.py
    │           │   │   │       │   ├── service_accounts
    │           │   │   │       │   │   ├── __init__.py
    │           │   │   │       │   │   ├── api_keys.py
    │           │   │   │       │   │   └── service_accounts.py
    │           │   │   │       │   ├── service_tier_settings.py
    │           │   │   │       │   ├── spend_alerts.py
    │           │   │   │       │   ├── spend_limit.py
    │           │   │   │       │   └── users
    │           │   │   │       │       ├── __init__.py
    │           │   │   │       │       ├── roles.py
    │           │   │   │       │       └── users.py
    │           │   │   │       ├── roles.py
    │           │   │   │       ├── spend_alerts.py
    │           │   │   │       ├── spend_limit.py
    │           │   │   │       ├── usage.py
    │           │   │   │       ├── users
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── roles.py
    │           │   │   │       │   └── users.py
    │           │   │   │       └── workload_identity_providers
    │           │   │   │           ├── __init__.py
    │           │   │   │           ├── federation_rules.py
    │           │   │   │           └── workload_identity_providers.py
    │           │   │   ├── audio
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── audio.py
    │           │   │   │   ├── speech.py
    │           │   │   │   ├── transcriptions.py
    │           │   │   │   ├── translations.py
    │           │   │   │   ├── voice_consents.py
    │           │   │   │   └── voices.py
    │           │   │   ├── batches.py
    │           │   │   ├── beta
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── agents
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── agents.py
    │           │   │   │   │   ├── automations
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── automations.py
    │           │   │   │   │   │   └── invocations.py
    │           │   │   │   │   ├── environments
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── environments.py
    │           │   │   │   │   │   ├── files.py
    │           │   │   │   │   │   └── templates.py
    │           │   │   │   │   ├── sessions
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── artifacts.py
    │           │   │   │   │   │   ├── events.py
    │           │   │   │   │   │   ├── items.py
    │           │   │   │   │   │   ├── sessions.py
    │           │   │   │   │   │   ├── subagents
    │           │   │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   │   ├── items.py
    │           │   │   │   │   │   │   ├── subagents.py
    │           │   │   │   │   │   │   └── turns
    │           │   │   │   │   │   │       ├── __init__.py
    │           │   │   │   │   │   │       ├── items.py
    │           │   │   │   │   │   │       └── turns.py
    │           │   │   │   │   │   ├── traces.py
    │           │   │   │   │   │   └── turns
    │           │   │   │   │   │       ├── __init__.py
    │           │   │   │   │   │       ├── items.py
    │           │   │   │   │   │       └── turns.py
    │           │   │   │   │   └── vaults
    │           │   │   │   │       ├── __init__.py
    │           │   │   │   │       ├── credentials.py
    │           │   │   │   │       └── vaults.py
    │           │   │   │   ├── assistants.py
    │           │   │   │   ├── beta.py
    │           │   │   │   ├── chatkit
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── chatkit.py
    │           │   │   │   │   ├── sessions.py
    │           │   │   │   │   └── threads.py
    │           │   │   │   ├── realtime
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── realtime.py
    │           │   │   │   │   ├── sessions.py
    │           │   │   │   │   └── transcription_sessions.py
    │           │   │   │   ├── responses
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── input_items.py
    │           │   │   │   │   ├── input_tokens.py
    │           │   │   │   │   └── responses.py
    │           │   │   │   └── threads
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── messages.py
    │           │   │   │       ├── runs
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── runs.py
    │           │   │   │       │   └── steps.py
    │           │   │   │       └── threads.py
    │           │   │   ├── chat
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── chat.py
    │           │   │   │   └── completions
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── completions.py
    │           │   │   │       └── messages.py
    │           │   │   ├── completions.py
    │           │   │   ├── containers
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── containers.py
    │           │   │   │   └── files
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── content.py
    │           │   │   │       └── files.py
    │           │   │   ├── content_provenance_checks.py
    │           │   │   ├── conversations
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.md
    │           │   │   │   ├── conversations.py
    │           │   │   │   └── items.py
    │           │   │   ├── decisions.py
    │           │   │   ├── embeddings.py
    │           │   │   ├── evals
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── evals.py
    │           │   │   │   └── runs
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── output_items.py
    │           │   │   │       └── runs.py
    │           │   │   ├── files.py
    │           │   │   ├── fine_tuning
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── alpha
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── alpha.py
    │           │   │   │   │   └── graders.py
    │           │   │   │   ├── checkpoints
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── checkpoints.py
    │           │   │   │   │   └── permissions.py
    │           │   │   │   ├── fine_tuning.py
    │           │   │   │   └── jobs
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── checkpoints.py
    │           │   │   │       └── jobs.py
    │           │   │   ├── images.py
    │           │   │   ├── live
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.md
    │           │   │   │   ├── forks.py
    │           │   │   │   ├── live.py
    │           │   │   │   ├── sessions.py
    │           │   │   │   └── sideband.py
    │           │   │   ├── models.py
    │           │   │   ├── moderations.py
    │           │   │   ├── realtime
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.md
    │           │   │   │   ├── calls.py
    │           │   │   │   ├── client_secrets.py
    │           │   │   │   ├── realtime.py
    │           │   │   │   └── translations
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── client_secrets.py
    │           │   │   │       └── translations.py
    │           │   │   ├── responses
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.md
    │           │   │   │   ├── input_items.py
    │           │   │   │   ├── input_tokens.py
    │           │   │   │   └── responses.py
    │           │   │   ├── safety
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── alerts.py
    │           │   │   │   ├── cases.py
    │           │   │   │   └── safety.py
    │           │   │   ├── skills
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── content.py
    │           │   │   │   ├── skills.py
    │           │   │   │   └── versions
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── content.py
    │           │   │   │       └── versions.py
    │           │   │   ├── uploads
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── parts.py
    │           │   │   │   └── uploads.py
    │           │   │   ├── vector_stores
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── file_batches.py
    │           │   │   │   ├── files.py
    │           │   │   │   └── vector_stores.py
    │           │   │   ├── videos.py
    │           │   │   └── webhooks
    │           │   │       ├── __init__.py
    │           │   │       ├── api.md
    │           │   │       ├── event_types.py
    │           │   │       └── webhooks.py
    │           │   ├── types
    │           │   │   ├── __init__.py
    │           │   │   ├── admin
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── organization
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── admin_api_key.py
    │           │   │   │       ├── admin_api_key_create_params.py
    │           │   │   │       ├── admin_api_key_create_response.py
    │           │   │   │       ├── admin_api_key_delete_response.py
    │           │   │   │       ├── admin_api_key_list_params.py
    │           │   │   │       ├── audit_log_list_params.py
    │           │   │   │       ├── audit_log_list_response.py
    │           │   │   │       ├── aws_external_storage_provider.py
    │           │   │   │       ├── azure_external_storage_provider.py
    │           │   │   │       ├── certificate.py
    │           │   │   │       ├── certificate_activate_params.py
    │           │   │   │       ├── certificate_activate_response.py
    │           │   │   │       ├── certificate_create_params.py
    │           │   │   │       ├── certificate_deactivate_params.py
    │           │   │   │       ├── certificate_deactivate_response.py
    │           │   │   │       ├── certificate_delete_response.py
    │           │   │   │       ├── certificate_list_params.py
    │           │   │   │       ├── certificate_list_response.py
    │           │   │   │       ├── certificate_retrieve_params.py
    │           │   │   │       ├── certificate_update_params.py
    │           │   │   │       ├── cost_quantity_unit.py
    │           │   │   │       ├── data_retention_update_params.py
    │           │   │   │       ├── external_key.py
    │           │   │   │       ├── external_key_create_params.py
    │           │   │   │       ├── external_key_list_params.py
    │           │   │   │       ├── external_key_validate_response.py
    │           │   │   │       ├── external_storage_configuration.py
    │           │   │   │       ├── external_storage_create_params.py
    │           │   │   │       ├── external_storage_deleted.py
    │           │   │   │       ├── external_storage_list_params.py
    │           │   │   │       ├── gcp_external_storage_provider.py
    │           │   │   │       ├── group.py
    │           │   │   │       ├── group_create_params.py
    │           │   │   │       ├── group_delete_response.py
    │           │   │   │       ├── group_list_params.py
    │           │   │   │       ├── group_update_params.py
    │           │   │   │       ├── group_update_response.py
    │           │   │   │       ├── groups
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── organization_group_user.py
    │           │   │   │       │   ├── role_create_params.py
    │           │   │   │       │   ├── role_create_response.py
    │           │   │   │       │   ├── role_delete_response.py
    │           │   │   │       │   ├── role_list_params.py
    │           │   │   │       │   ├── role_list_response.py
    │           │   │   │       │   ├── role_retrieve_response.py
    │           │   │   │       │   ├── user_create_params.py
    │           │   │   │       │   ├── user_create_response.py
    │           │   │   │       │   ├── user_delete_response.py
    │           │   │   │       │   ├── user_list_params.py
    │           │   │   │       │   └── user_retrieve_response.py
    │           │   │   │       ├── invite.py
    │           │   │   │       ├── invite_create_params.py
    │           │   │   │       ├── invite_delete_response.py
    │           │   │   │       ├── invite_list_params.py
    │           │   │   │       ├── oci_external_storage_provider.py
    │           │   │   │       ├── organization_data_retention.py
    │           │   │   │       ├── organization_spend_alert.py
    │           │   │   │       ├── organization_spend_alert_deleted.py
    │           │   │   │       ├── organization_spend_limit.py
    │           │   │   │       ├── organization_spend_limit_deleted.py
    │           │   │   │       ├── organization_user.py
    │           │   │   │       ├── project.py
    │           │   │   │       ├── project_create_params.py
    │           │   │   │       ├── project_list_params.py
    │           │   │   │       ├── project_residency.py
    │           │   │   │       ├── project_update_params.py
    │           │   │   │       ├── projects
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── api_key_delete_response.py
    │           │   │   │       │   ├── api_key_list_params.py
    │           │   │   │       │   ├── api_key_update_params.py
    │           │   │   │       │   ├── certificate_activate_params.py
    │           │   │   │       │   ├── certificate_activate_response.py
    │           │   │   │       │   ├── certificate_deactivate_params.py
    │           │   │   │       │   ├── certificate_deactivate_response.py
    │           │   │   │       │   ├── certificate_list_params.py
    │           │   │   │       │   ├── certificate_list_response.py
    │           │   │   │       │   ├── data_retention_update_params.py
    │           │   │   │       │   ├── group_create_params.py
    │           │   │   │       │   ├── group_delete_response.py
    │           │   │   │       │   ├── group_list_params.py
    │           │   │   │       │   ├── group_retrieve_params.py
    │           │   │   │       │   ├── groups
    │           │   │   │       │   │   ├── __init__.py
    │           │   │   │       │   │   ├── role_create_params.py
    │           │   │   │       │   │   ├── role_create_response.py
    │           │   │   │       │   │   ├── role_delete_response.py
    │           │   │   │       │   │   ├── role_list_params.py
    │           │   │   │       │   │   ├── role_list_response.py
    │           │   │   │       │   │   └── role_retrieve_response.py
    │           │   │   │       │   ├── hosted_tool_permission_update_params.py
    │           │   │   │       │   ├── model_permission_update_params.py
    │           │   │   │       │   ├── project_api_key.py
    │           │   │   │       │   ├── project_data_retention.py
    │           │   │   │       │   ├── project_group.py
    │           │   │   │       │   ├── project_hosted_tool_permissions.py
    │           │   │   │       │   ├── project_model_permissions.py
    │           │   │   │       │   ├── project_model_permissions_deleted.py
    │           │   │   │       │   ├── project_optional_service_tier.py
    │           │   │   │       │   ├── project_rate_limit.py
    │           │   │   │       │   ├── project_service_account.py
    │           │   │   │       │   ├── project_service_tier_settings.py
    │           │   │   │       │   ├── project_spend_alert.py
    │           │   │   │       │   ├── project_spend_alert_deleted.py
    │           │   │   │       │   ├── project_spend_limit.py
    │           │   │   │       │   ├── project_spend_limit_deleted.py
    │           │   │   │       │   ├── project_user.py
    │           │   │   │       │   ├── rate_limit_list_rate_limits_params.py
    │           │   │   │       │   ├── rate_limit_update_rate_limit_params.py
    │           │   │   │       │   ├── role_create_params.py
    │           │   │   │       │   ├── role_delete_response.py
    │           │   │   │       │   ├── role_list_params.py
    │           │   │   │       │   ├── role_update_params.py
    │           │   │   │       │   ├── service_account_create_params.py
    │           │   │   │       │   ├── service_account_create_response.py
    │           │   │   │       │   ├── service_account_delete_response.py
    │           │   │   │       │   ├── service_account_list_params.py
    │           │   │   │       │   ├── service_account_update_params.py
    │           │   │   │       │   ├── service_accounts
    │           │   │   │       │   │   ├── __init__.py
    │           │   │   │       │   │   ├── api_key_create_params.py
    │           │   │   │       │   │   └── api_key_create_response.py
    │           │   │   │       │   ├── service_tier_setting_update_params.py
    │           │   │   │       │   ├── spend_alert_create_params.py
    │           │   │   │       │   ├── spend_alert_list_params.py
    │           │   │   │       │   ├── spend_alert_update_params.py
    │           │   │   │       │   ├── spend_limit_update_params.py
    │           │   │   │       │   ├── user_create_params.py
    │           │   │   │       │   ├── user_delete_response.py
    │           │   │   │       │   ├── user_list_params.py
    │           │   │   │       │   ├── user_update_params.py
    │           │   │   │       │   └── users
    │           │   │   │       │       ├── __init__.py
    │           │   │   │       │       ├── role_create_params.py
    │           │   │   │       │       ├── role_create_response.py
    │           │   │   │       │       ├── role_delete_response.py
    │           │   │   │       │       ├── role_list_params.py
    │           │   │   │       │       ├── role_list_response.py
    │           │   │   │       │       └── role_retrieve_response.py
    │           │   │   │       ├── role.py
    │           │   │   │       ├── role_create_params.py
    │           │   │   │       ├── role_delete_response.py
    │           │   │   │       ├── role_list_params.py
    │           │   │   │       ├── role_update_params.py
    │           │   │   │       ├── spend_alert_create_params.py
    │           │   │   │       ├── spend_alert_list_params.py
    │           │   │   │       ├── spend_alert_update_params.py
    │           │   │   │       ├── spend_limit_update_params.py
    │           │   │   │       ├── usage_audio_speeches_params.py
    │           │   │   │       ├── usage_audio_speeches_response.py
    │           │   │   │       ├── usage_audio_transcriptions_params.py
    │           │   │   │       ├── usage_audio_transcriptions_response.py
    │           │   │   │       ├── usage_code_interpreter_sessions_params.py
    │           │   │   │       ├── usage_code_interpreter_sessions_response.py
    │           │   │   │       ├── usage_completions_params.py
    │           │   │   │       ├── usage_completions_response.py
    │           │   │   │       ├── usage_costs_params.py
    │           │   │   │       ├── usage_costs_response.py
    │           │   │   │       ├── usage_decisions_params.py
    │           │   │   │       ├── usage_decisions_response.py
    │           │   │   │       ├── usage_embeddings_params.py
    │           │   │   │       ├── usage_embeddings_response.py
    │           │   │   │       ├── usage_file_search_calls_params.py
    │           │   │   │       ├── usage_file_search_calls_response.py
    │           │   │   │       ├── usage_images_params.py
    │           │   │   │       ├── usage_images_response.py
    │           │   │   │       ├── usage_moderations_params.py
    │           │   │   │       ├── usage_moderations_response.py
    │           │   │   │       ├── usage_vector_stores_params.py
    │           │   │   │       ├── usage_vector_stores_response.py
    │           │   │   │       ├── usage_web_search_calls_params.py
    │           │   │   │       ├── usage_web_search_calls_response.py
    │           │   │   │       ├── user_delete_response.py
    │           │   │   │       ├── user_list_params.py
    │           │   │   │       ├── user_update_params.py
    │           │   │   │       ├── users
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── role_create_params.py
    │           │   │   │       │   ├── role_create_response.py
    │           │   │   │       │   ├── role_delete_response.py
    │           │   │   │       │   ├── role_list_params.py
    │           │   │   │       │   ├── role_list_response.py
    │           │   │   │       │   └── role_retrieve_response.py
    │           │   │   │       ├── workload_identity_provider.py
    │           │   │   │       ├── workload_identity_provider_create_params.py
    │           │   │   │       ├── workload_identity_provider_deleted.py
    │           │   │   │       ├── workload_identity_provider_list_params.py
    │           │   │   │       ├── workload_identity_provider_update_params.py
    │           │   │   │       └── workload_identity_providers
    │           │   │   │           ├── __init__.py
    │           │   │   │           ├── federation_rule.py
    │           │   │   │           ├── federation_rule_create_params.py
    │           │   │   │           ├── federation_rule_deleted.py
    │           │   │   │           ├── federation_rule_list_params.py
    │           │   │   │           └── federation_rule_update_params.py
    │           │   │   ├── audio
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── speech_create_params.py
    │           │   │   │   ├── speech_model.py
    │           │   │   │   ├── transcription.py
    │           │   │   │   ├── transcription_create_params.py
    │           │   │   │   ├── transcription_create_response.py
    │           │   │   │   ├── transcription_diarized.py
    │           │   │   │   ├── transcription_diarized_segment.py
    │           │   │   │   ├── transcription_include.py
    │           │   │   │   ├── transcription_language.py
    │           │   │   │   ├── transcription_segment.py
    │           │   │   │   ├── transcription_stream_event.py
    │           │   │   │   ├── transcription_text_delta_event.py
    │           │   │   │   ├── transcription_text_done_event.py
    │           │   │   │   ├── transcription_text_segment_event.py
    │           │   │   │   ├── transcription_verbose.py
    │           │   │   │   ├── transcription_word.py
    │           │   │   │   ├── translation.py
    │           │   │   │   ├── translation_create_params.py
    │           │   │   │   ├── translation_create_response.py
    │           │   │   │   ├── translation_verbose.py
    │           │   │   │   ├── voice.py
    │           │   │   │   ├── voice_consent.py
    │           │   │   │   ├── voice_consent_create_params.py
    │           │   │   │   ├── voice_consent_deleted.py
    │           │   │   │   ├── voice_consent_list_params.py
    │           │   │   │   ├── voice_consent_update_params.py
    │           │   │   │   ├── voice_create_params.py
    │           │   │   │   └── voice_deleted.py
    │           │   │   ├── audio_model.py
    │           │   │   ├── audio_response_format.py
    │           │   │   ├── auto_file_chunking_strategy_param.py
    │           │   │   ├── batch.py
    │           │   │   ├── batch_create_params.py
    │           │   │   ├── batch_error.py
    │           │   │   ├── batch_list_params.py
    │           │   │   ├── batch_request_counts.py
    │           │   │   ├── batch_usage.py
    │           │   │   ├── beta
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── agent.py
    │           │   │   │   ├── agent_browser_authentication_cancel_param.py
    │           │   │   │   ├── agent_browser_authentication_cancel_param_param.py
    │           │   │   │   ├── agent_browser_authentication_submit_param.py
    │           │   │   │   ├── agent_browser_authentication_submit_param_param.py
    │           │   │   │   ├── agent_browser_origin_access_param.py
    │           │   │   │   ├── agent_browser_origin_access_param_param.py
    │           │   │   │   ├── agent_close_subagent_call_item.py
    │           │   │   │   ├── agent_command_execution_item.py
    │           │   │   │   ├── agent_content.py
    │           │   │   │   ├── agent_create_params.py
    │           │   │   │   ├── agent_create_subagent_call_item.py
    │           │   │   │   ├── agent_deleted.py
    │           │   │   │   ├── agent_function_call_item.py
    │           │   │   │   ├── agent_function_call_output.py
    │           │   │   │   ├── agent_function_call_output_param.py
    │           │   │   │   ├── agent_function_call_status.py
    │           │   │   │   ├── agent_interrupt_subagent_call_item.py
    │           │   │   │   ├── agent_list_params.py
    │           │   │   │   ├── agent_mcp_call_item.py
    │           │   │   │   ├── agent_output_command_execution_output_delta_event.py
    │           │   │   │   ├── agent_output_item.py
    │           │   │   │   ├── agent_output_item_status.py
    │           │   │   │   ├── agent_reasoning.py
    │           │   │   │   ├── agent_reasoning_item.py
    │           │   │   │   ├── agent_reasoning_param.py
    │           │   │   │   ├── agent_resume_subagent_call_item.py
    │           │   │   │   ├── agent_send_subagent_input_call_item.py
    │           │   │   │   ├── agent_session.py
    │           │   │   │   ├── agent_session_assistant_message.py
    │           │   │   │   ├── agent_session_created_event.py
    │           │   │   │   ├── agent_session_deleted.py
    │           │   │   │   ├── agent_session_environment_connected_event.py
    │           │   │   │   ├── agent_session_environment_disconnected_event.py
    │           │   │   │   ├── agent_session_environment_expired_event.py
    │           │   │   │   ├── agent_session_environment_failed_event.py
    │           │   │   │   ├── agent_session_environment_pending_event.py
    │           │   │   │   ├── agent_session_environment_ready_event.py
    │           │   │   │   ├── agent_session_environment_reset_event.py
    │           │   │   │   ├── agent_session_environment_state.py
    │           │   │   │   ├── agent_session_environment_suspended_event.py
    │           │   │   │   ├── agent_session_error_event.py
    │           │   │   │   ├── agent_session_event.py
    │           │   │   │   ├── agent_session_failed_event.py
    │           │   │   │   ├── agent_session_idle_event.py
    │           │   │   │   ├── agent_session_in_progress_event.py
    │           │   │   │   ├── agent_session_input_message_param.py
    │           │   │   │   ├── agent_session_input_param.py
    │           │   │   │   ├── agent_session_item.py
    │           │   │   │   ├── agent_session_message.py
    │           │   │   │   ├── agent_session_message_content.py
    │           │   │   │   ├── agent_session_requires_action_event.py
    │           │   │   │   ├── agent_session_subagent_active_event.py
    │           │   │   │   ├── agent_session_subagent_closed_event.py
    │           │   │   │   ├── agent_session_subagent_created_event.py
    │           │   │   │   ├── agent_session_turn_cancelled_event.py
    │           │   │   │   ├── agent_session_turn_completed_event.py
    │           │   │   │   ├── agent_session_turn_content_part_added_event.py
    │           │   │   │   ├── agent_session_turn_content_part_done_event.py
    │           │   │   │   ├── agent_session_turn_created_event.py
    │           │   │   │   ├── agent_session_turn_failed_event.py
    │           │   │   │   ├── agent_session_turn_in_progress_event.py
    │           │   │   │   ├── agent_session_turn_item_added_event.py
    │           │   │   │   ├── agent_session_turn_item_done_event.py
    │           │   │   │   ├── agent_session_turn_output_text_delta_event.py
    │           │   │   │   ├── agent_session_turn_output_text_done_event.py
    │           │   │   │   ├── agent_session_turn_reasoning_summary_part_added_event.py
    │           │   │   │   ├── agent_session_turn_reasoning_summary_part_done_event.py
    │           │   │   │   ├── agent_session_turn_reasoning_summary_text_delta_event.py
    │           │   │   │   ├── agent_session_turn_reasoning_summary_text_done_event.py
    │           │   │   │   ├── agent_text.py
    │           │   │   │   ├── agent_text_param.py
    │           │   │   │   ├── agent_tool.py
    │           │   │   │   ├── agent_tool_param.py
    │           │   │   │   ├── agent_update_params.py
    │           │   │   │   ├── agent_wait_for_subagents_call_item.py
    │           │   │   │   ├── agent_web_search_call_item.py
    │           │   │   │   ├── agents
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── automation.py
    │           │   │   │   │   ├── automation_agent_config.py
    │           │   │   │   │   ├── automation_create_params.py
    │           │   │   │   │   ├── automation_created_by.py
    │           │   │   │   │   ├── automation_deleted.py
    │           │   │   │   │   ├── automation_environment.py
    │           │   │   │   │   ├── automation_list_params.py
    │           │   │   │   │   ├── automation_metadata_param.py
    │           │   │   │   │   ├── automation_target.py
    │           │   │   │   │   ├── automation_target_param.py
    │           │   │   │   │   ├── automation_update_params.py
    │           │   │   │   │   ├── automations
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── automation_invocation.py
    │           │   │   │   │   │   ├── automation_invocation_source.py
    │           │   │   │   │   │   └── invocation_list_params.py
    │           │   │   │   │   ├── environment_create_params.py
    │           │   │   │   │   ├── environment_info.py
    │           │   │   │   │   ├── environment_list_params.py
    │           │   │   │   │   ├── environments
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── environment_file.py
    │           │   │   │   │   │   ├── environment_template.py
    │           │   │   │   │   │   ├── environment_template_deleted.py
    │           │   │   │   │   │   ├── file_create_params.py
    │           │   │   │   │   │   ├── file_list_params.py
    │           │   │   │   │   │   ├── template_create_params.py
    │           │   │   │   │   │   ├── template_list_params.py
    │           │   │   │   │   │   └── template_update_params.py
    │           │   │   │   │   ├── one_time_automation.py
    │           │   │   │   │   ├── periodic_automation.py
    │           │   │   │   │   ├── session_create_params.py
    │           │   │   │   │   ├── session_list_params.py
    │           │   │   │   │   ├── session_update_params.py
    │           │   │   │   │   ├── sessions
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── artifact_list_params.py
    │           │   │   │   │   │   ├── event_create_params.py
    │           │   │   │   │   │   ├── event_stream_params.py
    │           │   │   │   │   │   ├── item_list_params.py
    │           │   │   │   │   │   ├── session_artifact.py
    │           │   │   │   │   │   ├── session_artifact_deleted.py
    │           │   │   │   │   │   ├── session_trace.py
    │           │   │   │   │   │   ├── subagent_list_params.py
    │           │   │   │   │   │   ├── subagents
    │           │   │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   │   ├── item_list_params.py
    │           │   │   │   │   │   │   ├── turn_list_params.py
    │           │   │   │   │   │   │   └── turns
    │           │   │   │   │   │   │       ├── __init__.py
    │           │   │   │   │   │   │       └── item_list_params.py
    │           │   │   │   │   │   ├── trace_list_params.py
    │           │   │   │   │   │   ├── turn.py
    │           │   │   │   │   │   ├── turn_list_params.py
    │           │   │   │   │   │   └── turns
    │           │   │   │   │   │       ├── __init__.py
    │           │   │   │   │   │       └── item_list_params.py
    │           │   │   │   │   ├── vault.py
    │           │   │   │   │   ├── vault_create_params.py
    │           │   │   │   │   ├── vault_deleted.py
    │           │   │   │   │   ├── vault_list_params.py
    │           │   │   │   │   ├── vault_status.py
    │           │   │   │   │   ├── vault_status_filter_param.py
    │           │   │   │   │   ├── vault_update_params.py
    │           │   │   │   │   └── vaults
    │           │   │   │   │       ├── __init__.py
    │           │   │   │   │       ├── credential.py
    │           │   │   │   │       ├── credential_auth.py
    │           │   │   │   │       ├── credential_auth_create_param.py
    │           │   │   │   │       ├── credential_auth_rotate_param.py
    │           │   │   │   │       ├── credential_create_params.py
    │           │   │   │   │       ├── credential_deleted.py
    │           │   │   │   │       ├── credential_list_params.py
    │           │   │   │   │       ├── credential_networking.py
    │           │   │   │   │       ├── credential_networking_param.py
    │           │   │   │   │       ├── credential_update_params.py
    │           │   │   │   │       ├── mcp_oauth_token_endpoint_auth.py
    │           │   │   │   │       ├── mcp_oauth_token_endpoint_auth_create_param.py
    │           │   │   │   │       └── mcp_oauth_token_endpoint_auth_rotate_param.py
    │           │   │   │   ├── assistant.py
    │           │   │   │   ├── assistant_create_params.py
    │           │   │   │   ├── assistant_deleted.py
    │           │   │   │   ├── assistant_list_params.py
    │           │   │   │   ├── assistant_response_format_option.py
    │           │   │   │   ├── assistant_response_format_option_param.py
    │           │   │   │   ├── assistant_stream_event.py
    │           │   │   │   ├── assistant_tool.py
    │           │   │   │   ├── assistant_tool_choice.py
    │           │   │   │   ├── assistant_tool_choice_function.py
    │           │   │   │   ├── assistant_tool_choice_function_param.py
    │           │   │   │   ├── assistant_tool_choice_option.py
    │           │   │   │   ├── assistant_tool_choice_option_param.py
    │           │   │   │   ├── assistant_tool_choice_param.py
    │           │   │   │   ├── assistant_tool_param.py
    │           │   │   │   ├── assistant_update_params.py
    │           │   │   │   ├── beta_apply_patch_tool.py
    │           │   │   │   ├── beta_apply_patch_tool_param.py
    │           │   │   │   ├── beta_compacted_response.py
    │           │   │   │   ├── beta_computer_action.py
    │           │   │   │   ├── beta_computer_action_list.py
    │           │   │   │   ├── beta_computer_action_list_param.py
    │           │   │   │   ├── beta_computer_action_param.py
    │           │   │   │   ├── beta_computer_tool.py
    │           │   │   │   ├── beta_computer_tool_param.py
    │           │   │   │   ├── beta_computer_use_preview_tool.py
    │           │   │   │   ├── beta_computer_use_preview_tool_param.py
    │           │   │   │   ├── beta_container_auto.py
    │           │   │   │   ├── beta_container_auto_param.py
    │           │   │   │   ├── beta_container_network_policy_allowlist.py
    │           │   │   │   ├── beta_container_network_policy_allowlist_param.py
    │           │   │   │   ├── beta_container_network_policy_disabled.py
    │           │   │   │   ├── beta_container_network_policy_disabled_param.py
    │           │   │   │   ├── beta_container_network_policy_domain_secret.py
    │           │   │   │   ├── beta_container_network_policy_domain_secret_param.py
    │           │   │   │   ├── beta_container_reference.py
    │           │   │   │   ├── beta_container_reference_param.py
    │           │   │   │   ├── beta_custom_tool.py
    │           │   │   │   ├── beta_custom_tool_param.py
    │           │   │   │   ├── beta_easy_input_message.py
    │           │   │   │   ├── beta_easy_input_message_param.py
    │           │   │   │   ├── beta_file_search_tool.py
    │           │   │   │   ├── beta_file_search_tool_param.py
    │           │   │   │   ├── beta_function_shell_tool.py
    │           │   │   │   ├── beta_function_shell_tool_param.py
    │           │   │   │   ├── beta_function_tool.py
    │           │   │   │   ├── beta_function_tool_param.py
    │           │   │   │   ├── beta_image_detail.py
    │           │   │   │   ├── beta_inline_skill.py
    │           │   │   │   ├── beta_inline_skill_param.py
    │           │   │   │   ├── beta_inline_skill_source.py
    │           │   │   │   ├── beta_inline_skill_source_param.py
    │           │   │   │   ├── beta_local_environment.py
    │           │   │   │   ├── beta_local_environment_param.py
    │           │   │   │   ├── beta_local_skill.py
    │           │   │   │   ├── beta_local_skill_param.py
    │           │   │   │   ├── beta_mcp_tool_call_error.py
    │           │   │   │   ├── beta_mcp_tool_call_error_param.py
    │           │   │   │   ├── beta_namespace_tool.py
    │           │   │   │   ├── beta_namespace_tool_param.py
    │           │   │   │   ├── beta_response.py
    │           │   │   │   ├── beta_response_apply_patch_tool_call.py
    │           │   │   │   ├── beta_response_apply_patch_tool_call_output.py
    │           │   │   │   ├── beta_response_audio_delta_event.py
    │           │   │   │   ├── beta_response_audio_done_event.py
    │           │   │   │   ├── beta_response_audio_transcript_delta_event.py
    │           │   │   │   ├── beta_response_audio_transcript_done_event.py
    │           │   │   │   ├── beta_response_code_interpreter_call_code_delta_event.py
    │           │   │   │   ├── beta_response_code_interpreter_call_code_done_event.py
    │           │   │   │   ├── beta_response_code_interpreter_call_completed_event.py
    │           │   │   │   ├── beta_response_code_interpreter_call_in_progress_event.py
    │           │   │   │   ├── beta_response_code_interpreter_call_interpreting_event.py
    │           │   │   │   ├── beta_response_code_interpreter_tool_call.py
    │           │   │   │   ├── beta_response_code_interpreter_tool_call_param.py
    │           │   │   │   ├── beta_response_compaction_compacting_event.py
    │           │   │   │   ├── beta_response_compaction_item.py
    │           │   │   │   ├── beta_response_compaction_item_param.py
    │           │   │   │   ├── beta_response_compaction_item_param_param.py
    │           │   │   │   ├── beta_response_completed_event.py
    │           │   │   │   ├── beta_response_computer_tool_call.py
    │           │   │   │   ├── beta_response_computer_tool_call_output_item.py
    │           │   │   │   ├── beta_response_computer_tool_call_output_screenshot.py
    │           │   │   │   ├── beta_response_computer_tool_call_output_screenshot_param.py
    │           │   │   │   ├── beta_response_computer_tool_call_param.py
    │           │   │   │   ├── beta_response_configuration_update_item.py
    │           │   │   │   ├── beta_response_configuration_update_item_param.py
    │           │   │   │   ├── beta_response_configuration_update_item_param_param.py
    │           │   │   │   ├── beta_response_container_reference.py
    │           │   │   │   ├── beta_response_content_part_added_event.py
    │           │   │   │   ├── beta_response_content_part_done_event.py
    │           │   │   │   ├── beta_response_conversation_param.py
    │           │   │   │   ├── beta_response_conversation_param_param.py
    │           │   │   │   ├── beta_response_created_event.py
    │           │   │   │   ├── beta_response_custom_tool_call.py
    │           │   │   │   ├── beta_response_custom_tool_call_input_delta_event.py
    │           │   │   │   ├── beta_response_custom_tool_call_input_done_event.py
    │           │   │   │   ├── beta_response_custom_tool_call_item.py
    │           │   │   │   ├── beta_response_custom_tool_call_output.py
    │           │   │   │   ├── beta_response_custom_tool_call_output_item.py
    │           │   │   │   ├── beta_response_custom_tool_call_output_param.py
    │           │   │   │   ├── beta_response_custom_tool_call_param.py
    │           │   │   │   ├── beta_response_error.py
    │           │   │   │   ├── beta_response_error_event.py
    │           │   │   │   ├── beta_response_failed_event.py
    │           │   │   │   ├── beta_response_file_search_call_completed_event.py
    │           │   │   │   ├── beta_response_file_search_call_in_progress_event.py
    │           │   │   │   ├── beta_response_file_search_call_searching_event.py
    │           │   │   │   ├── beta_response_file_search_tool_call.py
    │           │   │   │   ├── beta_response_file_search_tool_call_param.py
    │           │   │   │   ├── beta_response_format_text_config.py
    │           │   │   │   ├── beta_response_format_text_config_param.py
    │           │   │   │   ├── beta_response_format_text_json_schema_config.py
    │           │   │   │   ├── beta_response_format_text_json_schema_config_param.py
    │           │   │   │   ├── beta_response_function_call_arguments_delta_event.py
    │           │   │   │   ├── beta_response_function_call_arguments_done_event.py
    │           │   │   │   ├── beta_response_function_call_output_item.py
    │           │   │   │   ├── beta_response_function_call_output_item_list.py
    │           │   │   │   ├── beta_response_function_call_output_item_list_param.py
    │           │   │   │   ├── beta_response_function_call_output_item_param.py
    │           │   │   │   ├── beta_response_function_shell_call_output_content.py
    │           │   │   │   ├── beta_response_function_shell_call_output_content_param.py
    │           │   │   │   ├── beta_response_function_shell_tool_call.py
    │           │   │   │   ├── beta_response_function_shell_tool_call_output.py
    │           │   │   │   ├── beta_response_function_tool_call.py
    │           │   │   │   ├── beta_response_function_tool_call_item.py
    │           │   │   │   ├── beta_response_function_tool_call_output_item.py
    │           │   │   │   ├── beta_response_function_tool_call_param.py
    │           │   │   │   ├── beta_response_function_web_search.py
    │           │   │   │   ├── beta_response_function_web_search_param.py
    │           │   │   │   ├── beta_response_image_gen_call_completed_event.py
    │           │   │   │   ├── beta_response_image_gen_call_generating_event.py
    │           │   │   │   ├── beta_response_image_gen_call_in_progress_event.py
    │           │   │   │   ├── beta_response_image_gen_call_partial_image_event.py
    │           │   │   │   ├── beta_response_in_progress_event.py
    │           │   │   │   ├── beta_response_includable.py
    │           │   │   │   ├── beta_response_incomplete_event.py
    │           │   │   │   ├── beta_response_inject_created_event.py
    │           │   │   │   ├── beta_response_inject_event.py
    │           │   │   │   ├── beta_response_inject_event_param.py
    │           │   │   │   ├── beta_response_inject_failed_event.py
    │           │   │   │   ├── beta_response_input.py
    │           │   │   │   ├── beta_response_input_content.py
    │           │   │   │   ├── beta_response_input_content_param.py
    │           │   │   │   ├── beta_response_input_file.py
    │           │   │   │   ├── beta_response_input_file_content.py
    │           │   │   │   ├── beta_response_input_file_content_param.py
    │           │   │   │   ├── beta_response_input_file_param.py
    │           │   │   │   ├── beta_response_input_image.py
    │           │   │   │   ├── beta_response_input_image_content.py
    │           │   │   │   ├── beta_response_input_image_content_param.py
    │           │   │   │   ├── beta_response_input_image_param.py
    │           │   │   │   ├── beta_response_input_item.py
    │           │   │   │   ├── beta_response_input_item_param.py
    │           │   │   │   ├── beta_response_input_message_content_list.py
    │           │   │   │   ├── beta_response_input_message_content_list_param.py
    │           │   │   │   ├── beta_response_input_message_item.py
    │           │   │   │   ├── beta_response_input_param.py
    │           │   │   │   ├── beta_response_input_text.py
    │           │   │   │   ├── beta_response_input_text_content.py
    │           │   │   │   ├── beta_response_input_text_content_param.py
    │           │   │   │   ├── beta_response_input_text_param.py
    │           │   │   │   ├── beta_response_item.py
    │           │   │   │   ├── beta_response_local_environment.py
    │           │   │   │   ├── beta_response_mcp_call_arguments_delta_event.py
    │           │   │   │   ├── beta_response_mcp_call_arguments_done_event.py
    │           │   │   │   ├── beta_response_mcp_call_completed_event.py
    │           │   │   │   ├── beta_response_mcp_call_failed_event.py
    │           │   │   │   ├── beta_response_mcp_call_in_progress_event.py
    │           │   │   │   ├── beta_response_mcp_list_tools_completed_event.py
    │           │   │   │   ├── beta_response_mcp_list_tools_failed_event.py
    │           │   │   │   ├── beta_response_mcp_list_tools_in_progress_event.py
    │           │   │   │   ├── beta_response_output_item.py
    │           │   │   │   ├── beta_response_output_item_added_event.py
    │           │   │   │   ├── beta_response_output_item_done_event.py
    │           │   │   │   ├── beta_response_output_message.py
    │           │   │   │   ├── beta_response_output_message_param.py
    │           │   │   │   ├── beta_response_output_refusal.py
    │           │   │   │   ├── beta_response_output_refusal_param.py
    │           │   │   │   ├── beta_response_output_text.py
    │           │   │   │   ├── beta_response_output_text_annotation_added_event.py
    │           │   │   │   ├── beta_response_output_text_param.py
    │           │   │   │   ├── beta_response_prompt.py
    │           │   │   │   ├── beta_response_prompt_param.py
    │           │   │   │   ├── beta_response_queued_event.py
    │           │   │   │   ├── beta_response_reasoning_item.py
    │           │   │   │   ├── beta_response_reasoning_item_param.py
    │           │   │   │   ├── beta_response_reasoning_summary_part_added_event.py
    │           │   │   │   ├── beta_response_reasoning_summary_part_done_event.py
    │           │   │   │   ├── beta_response_reasoning_summary_text_delta_event.py
    │           │   │   │   ├── beta_response_reasoning_summary_text_done_event.py
    │           │   │   │   ├── beta_response_reasoning_text_delta_event.py
    │           │   │   │   ├── beta_response_reasoning_text_done_event.py
    │           │   │   │   ├── beta_response_refusal_delta_event.py
    │           │   │   │   ├── beta_response_refusal_done_event.py
    │           │   │   │   ├── beta_response_shell_call_command_added_event.py
    │           │   │   │   ├── beta_response_shell_call_command_delta_event.py
    │           │   │   │   ├── beta_response_shell_call_command_done_event.py
    │           │   │   │   ├── beta_response_shell_call_output_content_delta_event.py
    │           │   │   │   ├── beta_response_shell_call_output_content_done_event.py
    │           │   │   │   ├── beta_response_status.py
    │           │   │   │   ├── beta_response_steer_accepted_event.py
    │           │   │   │   ├── beta_response_steer_error_code.py
    │           │   │   │   ├── beta_response_steer_event.py
    │           │   │   │   ├── beta_response_steer_event_param.py
    │           │   │   │   ├── beta_response_steer_failed_event.py
    │           │   │   │   ├── beta_response_steer_input.py
    │           │   │   │   ├── beta_response_steer_input_content.py
    │           │   │   │   ├── beta_response_steer_input_content_param.py
    │           │   │   │   ├── beta_response_steer_input_param.py
    │           │   │   │   ├── beta_response_steer_pending_event.py
    │           │   │   │   ├── beta_response_steer_pending_reason.py
    │           │   │   │   ├── beta_response_steer_required_input.py
    │           │   │   │   ├── beta_response_stream_event.py
    │           │   │   │   ├── beta_response_text_config.py
    │           │   │   │   ├── beta_response_text_config_param.py
    │           │   │   │   ├── beta_response_text_delta_event.py
    │           │   │   │   ├── beta_response_text_done_event.py
    │           │   │   │   ├── beta_response_tool_search_call.py
    │           │   │   │   ├── beta_response_tool_search_output_item.py
    │           │   │   │   ├── beta_response_tool_search_output_item_param.py
    │           │   │   │   ├── beta_response_tool_search_output_item_param_param.py
    │           │   │   │   ├── beta_response_usage.py
    │           │   │   │   ├── beta_response_web_search_call_completed_event.py
    │           │   │   │   ├── beta_response_web_search_call_in_progress_event.py
    │           │   │   │   ├── beta_response_web_search_call_searching_event.py
    │           │   │   │   ├── beta_responses_client_event.py
    │           │   │   │   ├── beta_responses_client_event_param.py
    │           │   │   │   ├── beta_responses_server_event.py
    │           │   │   │   ├── beta_service_tier.py
    │           │   │   │   ├── beta_skill_reference.py
    │           │   │   │   ├── beta_skill_reference_param.py
    │           │   │   │   ├── beta_tool.py
    │           │   │   │   ├── beta_tool_choice_allowed.py
    │           │   │   │   ├── beta_tool_choice_allowed_param.py
    │           │   │   │   ├── beta_tool_choice_apply_patch.py
    │           │   │   │   ├── beta_tool_choice_apply_patch_param.py
    │           │   │   │   ├── beta_tool_choice_custom.py
    │           │   │   │   ├── beta_tool_choice_custom_param.py
    │           │   │   │   ├── beta_tool_choice_function.py
    │           │   │   │   ├── beta_tool_choice_function_param.py
    │           │   │   │   ├── beta_tool_choice_mcp.py
    │           │   │   │   ├── beta_tool_choice_mcp_param.py
    │           │   │   │   ├── beta_tool_choice_options.py
    │           │   │   │   ├── beta_tool_choice_shell.py
    │           │   │   │   ├── beta_tool_choice_shell_param.py
    │           │   │   │   ├── beta_tool_choice_types.py
    │           │   │   │   ├── beta_tool_choice_types_param.py
    │           │   │   │   ├── beta_tool_param.py
    │           │   │   │   ├── beta_tool_search_output_namespace_tool.py
    │           │   │   │   ├── beta_tool_search_output_namespace_tool_param.py
    │           │   │   │   ├── beta_tool_search_tool.py
    │           │   │   │   ├── beta_tool_search_tool_param.py
    │           │   │   │   ├── beta_web_search_preview_tool.py
    │           │   │   │   ├── beta_web_search_preview_tool_param.py
    │           │   │   │   ├── beta_web_search_tool.py
    │           │   │   │   ├── beta_web_search_tool_param.py
    │           │   │   │   ├── chat
    │           │   │   │   │   └── __init__.py
    │           │   │   │   ├── chatkit
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── chat_session.py
    │           │   │   │   │   ├── chat_session_automatic_thread_titling.py
    │           │   │   │   │   ├── chat_session_chatkit_configuration.py
    │           │   │   │   │   ├── chat_session_chatkit_configuration_param.py
    │           │   │   │   │   ├── chat_session_expires_after_param.py
    │           │   │   │   │   ├── chat_session_file_upload.py
    │           │   │   │   │   ├── chat_session_history.py
    │           │   │   │   │   ├── chat_session_rate_limits.py
    │           │   │   │   │   ├── chat_session_rate_limits_param.py
    │           │   │   │   │   ├── chat_session_status.py
    │           │   │   │   │   ├── chat_session_workflow_param.py
    │           │   │   │   │   ├── chatkit_attachment.py
    │           │   │   │   │   ├── chatkit_response_output_text.py
    │           │   │   │   │   ├── chatkit_thread.py
    │           │   │   │   │   ├── chatkit_thread_assistant_message_item.py
    │           │   │   │   │   ├── chatkit_thread_item_list.py
    │           │   │   │   │   ├── chatkit_thread_user_message_item.py
    │           │   │   │   │   ├── chatkit_widget_item.py
    │           │   │   │   │   ├── session_create_params.py
    │           │   │   │   │   ├── thread_delete_response.py
    │           │   │   │   │   ├── thread_list_items_params.py
    │           │   │   │   │   └── thread_list_params.py
    │           │   │   │   ├── chatkit_workflow.py
    │           │   │   │   ├── code_interpreter_tool.py
    │           │   │   │   ├── code_interpreter_tool_param.py
    │           │   │   │   ├── environment.py
    │           │   │   │   ├── environment_param.py
    │           │   │   │   ├── file_search_tool.py
    │           │   │   │   ├── file_search_tool_param.py
    │           │   │   │   ├── function_tool.py
    │           │   │   │   ├── function_tool_param.py
    │           │   │   │   ├── hosted_environment_file.py
    │           │   │   │   ├── hosted_environment_file_id.py
    │           │   │   │   ├── hosted_environment_file_param.py
    │           │   │   │   ├── hosted_plugin.py
    │           │   │   │   ├── hosted_plugin_param.py
    │           │   │   │   ├── hosted_skill.py
    │           │   │   │   ├── hosted_skill_param.py
    │           │   │   │   ├── hosted_skill_reference.py
    │           │   │   │   ├── inline_capability_source_param.py
    │           │   │   │   ├── input_content.py
    │           │   │   │   ├── input_content_param.py
    │           │   │   │   ├── mcp_transport.py
    │           │   │   │   ├── mcp_transport_param.py
    │           │   │   │   ├── multi_agent_config.py
    │           │   │   │   ├── multi_agent_config_param.py
    │           │   │   │   ├── output_text.py
    │           │   │   │   ├── persisted_agent_tool.py
    │           │   │   │   ├── persisted_agent_tool_param.py
    │           │   │   │   ├── persisted_mcp_transport.py
    │           │   │   │   ├── persisted_mcp_transport_param.py
    │           │   │   │   ├── realtime
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── conversation_created_event.py
    │           │   │   │   │   ├── conversation_item.py
    │           │   │   │   │   ├── conversation_item_content.py
    │           │   │   │   │   ├── conversation_item_content_param.py
    │           │   │   │   │   ├── conversation_item_create_event.py
    │           │   │   │   │   ├── conversation_item_create_event_param.py
    │           │   │   │   │   ├── conversation_item_created_event.py
    │           │   │   │   │   ├── conversation_item_delete_event.py
    │           │   │   │   │   ├── conversation_item_delete_event_param.py
    │           │   │   │   │   ├── conversation_item_deleted_event.py
    │           │   │   │   │   ├── conversation_item_input_audio_transcription_completed_event.py
    │           │   │   │   │   ├── conversation_item_input_audio_transcription_delta_event.py
    │           │   │   │   │   ├── conversation_item_input_audio_transcription_failed_event.py
    │           │   │   │   │   ├── conversation_item_param.py
    │           │   │   │   │   ├── conversation_item_retrieve_event.py
    │           │   │   │   │   ├── conversation_item_retrieve_event_param.py
    │           │   │   │   │   ├── conversation_item_truncate_event.py
    │           │   │   │   │   ├── conversation_item_truncate_event_param.py
    │           │   │   │   │   ├── conversation_item_truncated_event.py
    │           │   │   │   │   ├── conversation_item_with_reference.py
    │           │   │   │   │   ├── conversation_item_with_reference_param.py
    │           │   │   │   │   ├── error_event.py
    │           │   │   │   │   ├── input_audio_buffer_append_event.py
    │           │   │   │   │   ├── input_audio_buffer_append_event_param.py
    │           │   │   │   │   ├── input_audio_buffer_clear_event.py
    │           │   │   │   │   ├── input_audio_buffer_clear_event_param.py
    │           │   │   │   │   ├── input_audio_buffer_cleared_event.py
    │           │   │   │   │   ├── input_audio_buffer_commit_event.py
    │           │   │   │   │   ├── input_audio_buffer_commit_event_param.py
    │           │   │   │   │   ├── input_audio_buffer_committed_event.py
    │           │   │   │   │   ├── input_audio_buffer_speech_started_event.py
    │           │   │   │   │   ├── input_audio_buffer_speech_stopped_event.py
    │           │   │   │   │   ├── rate_limits_updated_event.py
    │           │   │   │   │   ├── realtime_client_event.py
    │           │   │   │   │   ├── realtime_client_event_param.py
    │           │   │   │   │   ├── realtime_connect_params.py
    │           │   │   │   │   ├── realtime_response.py
    │           │   │   │   │   ├── realtime_response_status.py
    │           │   │   │   │   ├── realtime_response_usage.py
    │           │   │   │   │   ├── realtime_server_event.py
    │           │   │   │   │   ├── response_audio_delta_event.py
    │           │   │   │   │   ├── response_audio_done_event.py
    │           │   │   │   │   ├── response_audio_transcript_delta_event.py
    │           │   │   │   │   ├── response_audio_transcript_done_event.py
    │           │   │   │   │   ├── response_cancel_event.py
    │           │   │   │   │   ├── response_cancel_event_param.py
    │           │   │   │   │   ├── response_content_part_added_event.py
    │           │   │   │   │   ├── response_content_part_done_event.py
    │           │   │   │   │   ├── response_create_event.py
    │           │   │   │   │   ├── response_create_event_param.py
    │           │   │   │   │   ├── response_created_event.py
    │           │   │   │   │   ├── response_done_event.py
    │           │   │   │   │   ├── response_function_call_arguments_delta_event.py
    │           │   │   │   │   ├── response_function_call_arguments_done_event.py
    │           │   │   │   │   ├── response_output_item_added_event.py
    │           │   │   │   │   ├── response_output_item_done_event.py
    │           │   │   │   │   ├── response_text_delta_event.py
    │           │   │   │   │   ├── response_text_done_event.py
    │           │   │   │   │   ├── session.py
    │           │   │   │   │   ├── session_create_params.py
    │           │   │   │   │   ├── session_create_response.py
    │           │   │   │   │   ├── session_created_event.py
    │           │   │   │   │   ├── session_update_event.py
    │           │   │   │   │   ├── session_update_event_param.py
    │           │   │   │   │   ├── session_updated_event.py
    │           │   │   │   │   ├── transcription_session.py
    │           │   │   │   │   ├── transcription_session_create_params.py
    │           │   │   │   │   ├── transcription_session_update.py
    │           │   │   │   │   ├── transcription_session_update_param.py
    │           │   │   │   │   └── transcription_session_updated_event.py
    │           │   │   │   ├── response_compact_params.py
    │           │   │   │   ├── response_create_params.py
    │           │   │   │   ├── response_retrieve_params.py
    │           │   │   │   ├── responses
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── beta_response_item_list.py
    │           │   │   │   │   ├── input_item_list_params.py
    │           │   │   │   │   ├── input_token_count_params.py
    │           │   │   │   │   └── input_token_count_response.py
    │           │   │   │   ├── session_error.py
    │           │   │   │   ├── session_turn_error.py
    │           │   │   │   ├── setup_command_param.py
    │           │   │   │   ├── subagent.py
    │           │   │   │   ├── summary_text.py
    │           │   │   │   ├── text_format.py
    │           │   │   │   ├── text_format_param.py
    │           │   │   │   ├── thread.py
    │           │   │   │   ├── thread_create_and_run_params.py
    │           │   │   │   ├── thread_create_params.py
    │           │   │   │   ├── thread_deleted.py
    │           │   │   │   ├── thread_update_params.py
    │           │   │   │   ├── threads
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── annotation.py
    │           │   │   │   │   ├── annotation_delta.py
    │           │   │   │   │   ├── file_citation_annotation.py
    │           │   │   │   │   ├── file_citation_delta_annotation.py
    │           │   │   │   │   ├── file_path_annotation.py
    │           │   │   │   │   ├── file_path_delta_annotation.py
    │           │   │   │   │   ├── image_file.py
    │           │   │   │   │   ├── image_file_content_block.py
    │           │   │   │   │   ├── image_file_content_block_param.py
    │           │   │   │   │   ├── image_file_delta.py
    │           │   │   │   │   ├── image_file_delta_block.py
    │           │   │   │   │   ├── image_file_param.py
    │           │   │   │   │   ├── image_url.py
    │           │   │   │   │   ├── image_url_content_block.py
    │           │   │   │   │   ├── image_url_content_block_param.py
    │           │   │   │   │   ├── image_url_delta.py
    │           │   │   │   │   ├── image_url_delta_block.py
    │           │   │   │   │   ├── image_url_param.py
    │           │   │   │   │   ├── message.py
    │           │   │   │   │   ├── message_content.py
    │           │   │   │   │   ├── message_content_delta.py
    │           │   │   │   │   ├── message_content_part_param.py
    │           │   │   │   │   ├── message_create_params.py
    │           │   │   │   │   ├── message_deleted.py
    │           │   │   │   │   ├── message_delta.py
    │           │   │   │   │   ├── message_delta_event.py
    │           │   │   │   │   ├── message_list_params.py
    │           │   │   │   │   ├── message_update_params.py
    │           │   │   │   │   ├── refusal_content_block.py
    │           │   │   │   │   ├── refusal_delta_block.py
    │           │   │   │   │   ├── required_action_function_tool_call.py
    │           │   │   │   │   ├── run.py
    │           │   │   │   │   ├── run_create_params.py
    │           │   │   │   │   ├── run_list_params.py
    │           │   │   │   │   ├── run_status.py
    │           │   │   │   │   ├── run_submit_tool_outputs_params.py
    │           │   │   │   │   ├── run_update_params.py
    │           │   │   │   │   ├── runs
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── code_interpreter_logs.py
    │           │   │   │   │   │   ├── code_interpreter_output_image.py
    │           │   │   │   │   │   ├── code_interpreter_tool_call.py
    │           │   │   │   │   │   ├── code_interpreter_tool_call_delta.py
    │           │   │   │   │   │   ├── file_search_tool_call.py
    │           │   │   │   │   │   ├── file_search_tool_call_delta.py
    │           │   │   │   │   │   ├── function_tool_call.py
    │           │   │   │   │   │   ├── function_tool_call_delta.py
    │           │   │   │   │   │   ├── message_creation_step_details.py
    │           │   │   │   │   │   ├── run_step.py
    │           │   │   │   │   │   ├── run_step_delta.py
    │           │   │   │   │   │   ├── run_step_delta_event.py
    │           │   │   │   │   │   ├── run_step_delta_message_delta.py
    │           │   │   │   │   │   ├── run_step_include.py
    │           │   │   │   │   │   ├── step_list_params.py
    │           │   │   │   │   │   ├── step_retrieve_params.py
    │           │   │   │   │   │   ├── tool_call.py
    │           │   │   │   │   │   ├── tool_call_delta.py
    │           │   │   │   │   │   ├── tool_call_delta_object.py
    │           │   │   │   │   │   └── tool_calls_step_details.py
    │           │   │   │   │   ├── text.py
    │           │   │   │   │   ├── text_content_block.py
    │           │   │   │   │   ├── text_content_block_param.py
    │           │   │   │   │   ├── text_delta.py
    │           │   │   │   │   └── text_delta_block.py
    │           │   │   │   ├── token_usage.py
    │           │   │   │   └── web_search_action.py
    │           │   │   ├── chat
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── chat_completion.py
    │           │   │   │   ├── chat_completion_allowed_tool_choice_param.py
    │           │   │   │   ├── chat_completion_allowed_tools_param.py
    │           │   │   │   ├── chat_completion_assistant_message_param.py
    │           │   │   │   ├── chat_completion_audio.py
    │           │   │   │   ├── chat_completion_audio_param.py
    │           │   │   │   ├── chat_completion_chunk.py
    │           │   │   │   ├── chat_completion_content_part_image.py
    │           │   │   │   ├── chat_completion_content_part_image_param.py
    │           │   │   │   ├── chat_completion_content_part_input_audio_param.py
    │           │   │   │   ├── chat_completion_content_part_param.py
    │           │   │   │   ├── chat_completion_content_part_refusal_param.py
    │           │   │   │   ├── chat_completion_content_part_text.py
    │           │   │   │   ├── chat_completion_content_part_text_param.py
    │           │   │   │   ├── chat_completion_custom_tool_param.py
    │           │   │   │   ├── chat_completion_deleted.py
    │           │   │   │   ├── chat_completion_developer_message_param.py
    │           │   │   │   ├── chat_completion_function_call_option_param.py
    │           │   │   │   ├── chat_completion_function_message_param.py
    │           │   │   │   ├── chat_completion_function_tool.py
    │           │   │   │   ├── chat_completion_function_tool_param.py
    │           │   │   │   ├── chat_completion_message.py
    │           │   │   │   ├── chat_completion_message_custom_tool_call.py
    │           │   │   │   ├── chat_completion_message_custom_tool_call_param.py
    │           │   │   │   ├── chat_completion_message_function_tool_call.py
    │           │   │   │   ├── chat_completion_message_function_tool_call_param.py
    │           │   │   │   ├── chat_completion_message_param.py
    │           │   │   │   ├── chat_completion_message_tool_call.py
    │           │   │   │   ├── chat_completion_message_tool_call_param.py
    │           │   │   │   ├── chat_completion_message_tool_call_union_param.py
    │           │   │   │   ├── chat_completion_modality.py
    │           │   │   │   ├── chat_completion_named_tool_choice_custom_param.py
    │           │   │   │   ├── chat_completion_named_tool_choice_param.py
    │           │   │   │   ├── chat_completion_prediction_content_param.py
    │           │   │   │   ├── chat_completion_reasoning_effort.py
    │           │   │   │   ├── chat_completion_role.py
    │           │   │   │   ├── chat_completion_store_message.py
    │           │   │   │   ├── chat_completion_stream_options_param.py
    │           │   │   │   ├── chat_completion_system_message_param.py
    │           │   │   │   ├── chat_completion_token_logprob.py
    │           │   │   │   ├── chat_completion_tool_choice_option_param.py
    │           │   │   │   ├── chat_completion_tool_message_param.py
    │           │   │   │   ├── chat_completion_tool_param.py
    │           │   │   │   ├── chat_completion_tool_union_param.py
    │           │   │   │   ├── chat_completion_user_message_param.py
    │           │   │   │   ├── completion_create_params.py
    │           │   │   │   ├── completion_list_params.py
    │           │   │   │   ├── completion_update_params.py
    │           │   │   │   ├── completions
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── message_list_params.py
    │           │   │   │   ├── create_chat_completion_request_message_param.py
    │           │   │   │   ├── parsed_chat_completion.py
    │           │   │   │   └── parsed_function_tool_call.py
    │           │   │   ├── chat_model.py
    │           │   │   ├── completion.py
    │           │   │   ├── completion_choice.py
    │           │   │   ├── completion_create_params.py
    │           │   │   ├── completion_usage.py
    │           │   │   ├── container_create_params.py
    │           │   │   ├── container_create_response.py
    │           │   │   ├── container_list_params.py
    │           │   │   ├── container_list_response.py
    │           │   │   ├── container_retrieve_response.py
    │           │   │   ├── containers
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── file_create_params.py
    │           │   │   │   ├── file_create_response.py
    │           │   │   │   ├── file_list_params.py
    │           │   │   │   ├── file_list_response.py
    │           │   │   │   ├── file_retrieve_response.py
    │           │   │   │   └── files
    │           │   │   │       └── __init__.py
    │           │   │   ├── content_provenance_check.py
    │           │   │   ├── content_provenance_check_create_params.py
    │           │   │   ├── conversations
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── computer_screenshot_content.py
    │           │   │   │   ├── conversation.py
    │           │   │   │   ├── conversation_create_params.py
    │           │   │   │   ├── conversation_deleted_resource.py
    │           │   │   │   ├── conversation_item.py
    │           │   │   │   ├── conversation_item_list.py
    │           │   │   │   ├── conversation_update_params.py
    │           │   │   │   ├── input_file_content.py
    │           │   │   │   ├── input_file_content_param.py
    │           │   │   │   ├── input_image_content.py
    │           │   │   │   ├── input_image_content_param.py
    │           │   │   │   ├── input_text_content.py
    │           │   │   │   ├── input_text_content_param.py
    │           │   │   │   ├── item_create_params.py
    │           │   │   │   ├── item_list_params.py
    │           │   │   │   ├── item_retrieve_params.py
    │           │   │   │   ├── message.py
    │           │   │   │   ├── output_text_content.py
    │           │   │   │   ├── output_text_content_param.py
    │           │   │   │   ├── refusal_content.py
    │           │   │   │   ├── refusal_content_param.py
    │           │   │   │   ├── summary_text_content.py
    │           │   │   │   └── text_content.py
    │           │   │   ├── create_embedding_response.py
    │           │   │   ├── decision.py
    │           │   │   ├── decision_create_params.py
    │           │   │   ├── decision_input_image_param.py
    │           │   │   ├── decision_input_message_param.py
    │           │   │   ├── decision_input_part_union_param.py
    │           │   │   ├── decision_input_text_param.py
    │           │   │   ├── decision_prompt_cache_breakpoint_param.py
    │           │   │   ├── deleted_skill.py
    │           │   │   ├── embedding.py
    │           │   │   ├── embedding_create_params.py
    │           │   │   ├── embedding_model.py
    │           │   │   ├── eval_create_params.py
    │           │   │   ├── eval_create_response.py
    │           │   │   ├── eval_custom_data_source_config.py
    │           │   │   ├── eval_delete_response.py
    │           │   │   ├── eval_list_params.py
    │           │   │   ├── eval_list_response.py
    │           │   │   ├── eval_retrieve_response.py
    │           │   │   ├── eval_stored_completions_data_source_config.py
    │           │   │   ├── eval_update_params.py
    │           │   │   ├── eval_update_response.py
    │           │   │   ├── evals
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── create_eval_completions_run_data_source.py
    │           │   │   │   ├── create_eval_completions_run_data_source_param.py
    │           │   │   │   ├── create_eval_jsonl_run_data_source.py
    │           │   │   │   ├── create_eval_jsonl_run_data_source_param.py
    │           │   │   │   ├── eval_api_error.py
    │           │   │   │   ├── run_cancel_response.py
    │           │   │   │   ├── run_create_params.py
    │           │   │   │   ├── run_create_response.py
    │           │   │   │   ├── run_delete_response.py
    │           │   │   │   ├── run_list_params.py
    │           │   │   │   ├── run_list_response.py
    │           │   │   │   ├── run_retrieve_response.py
    │           │   │   │   └── runs
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── output_item_list_params.py
    │           │   │   │       ├── output_item_list_response.py
    │           │   │   │       └── output_item_retrieve_response.py
    │           │   │   ├── file_chunking_strategy.py
    │           │   │   ├── file_chunking_strategy_param.py
    │           │   │   ├── file_content.py
    │           │   │   ├── file_create_params.py
    │           │   │   ├── file_deleted.py
    │           │   │   ├── file_list_params.py
    │           │   │   ├── file_object.py
    │           │   │   ├── file_purpose.py
    │           │   │   ├── fine_tuning
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── alpha
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── grader_run_params.py
    │           │   │   │   │   ├── grader_run_response.py
    │           │   │   │   │   ├── grader_validate_params.py
    │           │   │   │   │   └── grader_validate_response.py
    │           │   │   │   ├── checkpoints
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── permission_create_params.py
    │           │   │   │   │   ├── permission_create_response.py
    │           │   │   │   │   ├── permission_delete_response.py
    │           │   │   │   │   ├── permission_list_params.py
    │           │   │   │   │   ├── permission_list_response.py
    │           │   │   │   │   ├── permission_retrieve_params.py
    │           │   │   │   │   └── permission_retrieve_response.py
    │           │   │   │   ├── dpo_hyperparameters.py
    │           │   │   │   ├── dpo_hyperparameters_param.py
    │           │   │   │   ├── dpo_method.py
    │           │   │   │   ├── dpo_method_param.py
    │           │   │   │   ├── fine_tuning_job.py
    │           │   │   │   ├── fine_tuning_job_event.py
    │           │   │   │   ├── fine_tuning_job_integration.py
    │           │   │   │   ├── fine_tuning_job_wandb_integration.py
    │           │   │   │   ├── fine_tuning_job_wandb_integration_object.py
    │           │   │   │   ├── job_create_params.py
    │           │   │   │   ├── job_list_events_params.py
    │           │   │   │   ├── job_list_params.py
    │           │   │   │   ├── jobs
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── checkpoint_list_params.py
    │           │   │   │   │   └── fine_tuning_job_checkpoint.py
    │           │   │   │   ├── reinforcement_hyperparameters.py
    │           │   │   │   ├── reinforcement_hyperparameters_param.py
    │           │   │   │   ├── reinforcement_method.py
    │           │   │   │   ├── reinforcement_method_param.py
    │           │   │   │   ├── supervised_hyperparameters.py
    │           │   │   │   ├── supervised_hyperparameters_param.py
    │           │   │   │   ├── supervised_method.py
    │           │   │   │   └── supervised_method_param.py
    │           │   │   ├── graders
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── grader_inputs.py
    │           │   │   │   ├── grader_inputs_param.py
    │           │   │   │   ├── label_model_grader.py
    │           │   │   │   ├── label_model_grader_param.py
    │           │   │   │   ├── multi_grader.py
    │           │   │   │   ├── multi_grader_param.py
    │           │   │   │   ├── python_grader.py
    │           │   │   │   ├── python_grader_param.py
    │           │   │   │   ├── score_model_grader.py
    │           │   │   │   ├── score_model_grader_param.py
    │           │   │   │   ├── string_check_grader.py
    │           │   │   │   ├── string_check_grader_param.py
    │           │   │   │   ├── text_similarity_grader.py
    │           │   │   │   └── text_similarity_grader_param.py
    │           │   │   ├── image.py
    │           │   │   ├── image_create_variation_params.py
    │           │   │   ├── image_edit_completed_event.py
    │           │   │   ├── image_edit_params.py
    │           │   │   ├── image_edit_partial_image_event.py
    │           │   │   ├── image_edit_stream_event.py
    │           │   │   ├── image_gen_completed_event.py
    │           │   │   ├── image_gen_partial_image_event.py
    │           │   │   ├── image_gen_stream_event.py
    │           │   │   ├── image_generate_params.py
    │           │   │   ├── image_input_reference_param.py
    │           │   │   ├── image_model.py
    │           │   │   ├── images_response.py
    │           │   │   ├── live
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── audio_format.py
    │           │   │   │   ├── audio_format_param.py
    │           │   │   │   ├── built_in_voice.py
    │           │   │   │   ├── client_config.py
    │           │   │   │   ├── client_config_param.py
    │           │   │   │   ├── client_delegation.py
    │           │   │   │   ├── client_delegation_param.py
    │           │   │   │   ├── client_event.py
    │           │   │   │   ├── client_event_param.py
    │           │   │   │   ├── commentary_append_event.py
    │           │   │   │   ├── commentary_append_event_param.py
    │           │   │   │   ├── commentary_appended_event.py
    │           │   │   │   ├── connect_client_event.py
    │           │   │   │   ├── connect_client_event_param.py
    │           │   │   │   ├── connect_server_event.py
    │           │   │   │   ├── custom_voice.py
    │           │   │   │   ├── custom_voice_param.py
    │           │   │   │   ├── data_channel_config.py
    │           │   │   │   ├── data_channel_config_param.py
    │           │   │   │   ├── decision_assistant_message.py
    │           │   │   │   ├── decision_assistant_message_param.py
    │           │   │   │   ├── decision_choice_option.py
    │           │   │   │   ├── decision_choice_option_param.py
    │           │   │   │   ├── decision_create_event.py
    │           │   │   │   ├── decision_create_event_param.py
    │           │   │   │   ├── decision_developer_message.py
    │           │   │   │   ├── decision_developer_message_param.py
    │           │   │   │   ├── decision_event.py
    │           │   │   │   ├── decision_input_text.py
    │           │   │   │   ├── decision_input_text_param.py
    │           │   │   │   ├── decision_item_create_event.py
    │           │   │   │   ├── decision_item_create_event_param.py
    │           │   │   │   ├── decision_item_created_event.py
    │           │   │   │   ├── decision_item_delete_event.py
    │           │   │   │   ├── decision_item_delete_event_param.py
    │           │   │   │   ├── decision_item_deleted_event.py
    │           │   │   │   ├── decision_json_object.py
    │           │   │   │   ├── decision_json_object_param.py
    │           │   │   │   ├── decision_question.py
    │           │   │   │   ├── decision_question_param.py
    │           │   │   │   ├── decision_stored_assistant_message.py
    │           │   │   │   ├── decision_stored_developer_message.py
    │           │   │   │   ├── decision_stored_system_message.py
    │           │   │   │   ├── decision_stored_user_message.py
    │           │   │   │   ├── decision_system_message.py
    │           │   │   │   ├── decision_system_message_param.py
    │           │   │   │   ├── decision_trigger.py
    │           │   │   │   ├── decision_trigger_param.py
    │           │   │   │   ├── decision_user_message.py
    │           │   │   │   ├── decision_user_message_param.py
    │           │   │   │   ├── decisions_delegation_config.py
    │           │   │   │   ├── decisions_delegation_config_param.py
    │           │   │   │   ├── decisions_delegation_update_config.py
    │           │   │   │   ├── decisions_delegation_update_config_param.py
    │           │   │   │   ├── delegation_created_event.py
    │           │   │   │   ├── error.py
    │           │   │   │   ├── error_event.py
    │           │   │   │   ├── fork_client_event.py
    │           │   │   │   ├── fork_client_event_param.py
    │           │   │   │   ├── fork_server_event.py
    │           │   │   │   ├── fork_session_config.py
    │           │   │   │   ├── fork_session_config_param.py
    │           │   │   │   ├── fork_session_start_event.py
    │           │   │   │   ├── fork_session_start_event_param.py
    │           │   │   │   ├── function_tool.py
    │           │   │   │   ├── function_tool_param.py
    │           │   │   │   ├── info_event.py
    │           │   │   │   ├── initial_item.py
    │           │   │   │   ├── initial_item_param.py
    │           │   │   │   ├── input_audio_append_event.py
    │           │   │   │   ├── input_audio_append_event_param.py
    │           │   │   │   ├── input_audio_mute_event.py
    │           │   │   │   ├── input_audio_mute_event_param.py
    │           │   │   │   ├── input_audio_muted_event.py
    │           │   │   │   ├── input_audio_unmute_event.py
    │           │   │   │   ├── input_audio_unmute_event_param.py
    │           │   │   │   ├── input_audio_unmuted_event.py
    │           │   │   │   ├── input_transcript_delta_event.py
    │           │   │   │   ├── instructions_append_event.py
    │           │   │   │   ├── instructions_append_event_param.py
    │           │   │   │   ├── instructions_appended_event.py
    │           │   │   │   ├── live_create_params.py
    │           │   │   │   ├── live_create_response.py
    │           │   │   │   ├── media_session_config_param.py
    │           │   │   │   ├── media_session_fork_config_param.py
    │           │   │   │   ├── output_audio_delta_event.py
    │           │   │   │   ├── output_audio_fixture_play_event.py
    │           │   │   │   ├── output_audio_fixture_play_event_param.py
    │           │   │   │   ├── output_audio_fixture_played_event.py
    │           │   │   │   ├── output_audio_fixture_playing_event.py
    │           │   │   │   ├── output_transcript_delta_event.py
    │           │   │   │   ├── response_create_event.py
    │           │   │   │   ├── response_create_event_param.py
    │           │   │   │   ├── response_event.py
    │           │   │   │   ├── response_item_create_event.py
    │           │   │   │   ├── response_item_create_event_param.py
    │           │   │   │   ├── responses_delegation_config.py
    │           │   │   │   ├── responses_delegation_config_param.py
    │           │   │   │   ├── responses_delegation_update_config.py
    │           │   │   │   ├── responses_delegation_update_config_param.py
    │           │   │   │   ├── server_event.py
    │           │   │   │   ├── server_event_selector.py
    │           │   │   │   ├── server_event_selector_param.py
    │           │   │   │   ├── session_accept_params.py
    │           │   │   │   ├── session_close_event.py
    │           │   │   │   ├── session_close_event_param.py
    │           │   │   │   ├── session_closed_event.py
    │           │   │   │   ├── session_config.py
    │           │   │   │   ├── session_config_param.py
    │           │   │   │   ├── session_fork_params.py
    │           │   │   │   ├── session_fork_response.py
    │           │   │   │   ├── session_refer_params.py
    │           │   │   │   ├── session_reject_params.py
    │           │   │   │   ├── session_resource.py
    │           │   │   │   ├── session_start_event.py
    │           │   │   │   ├── session_start_event_param.py
    │           │   │   │   ├── session_started_event.py
    │           │   │   │   ├── session_update_config.py
    │           │   │   │   ├── session_update_config_param.py
    │           │   │   │   ├── session_update_event.py
    │           │   │   │   ├── session_update_event_param.py
    │           │   │   │   ├── session_updated_event.py
    │           │   │   │   ├── session_usage.py
    │           │   │   │   ├── session_usage_updated_event.py
    │           │   │   │   ├── sideband_connect_params.py
    │           │   │   │   ├── thinking_append_event.py
    │           │   │   │   ├── thinking_append_event_param.py
    │           │   │   │   └── thinking_appended_event.py
    │           │   │   ├── model.py
    │           │   │   ├── model_deleted.py
    │           │   │   ├── moderation.py
    │           │   │   ├── moderation_create_params.py
    │           │   │   ├── moderation_create_response.py
    │           │   │   ├── moderation_image_url_input_param.py
    │           │   │   ├── moderation_model.py
    │           │   │   ├── moderation_multi_modal_input_param.py
    │           │   │   ├── moderation_text_input_param.py
    │           │   │   ├── other_file_chunking_strategy_object.py
    │           │   │   ├── realtime
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── audio_transcription.py
    │           │   │   │   ├── audio_transcription_param.py
    │           │   │   │   ├── call_accept_params.py
    │           │   │   │   ├── call_create_params.py
    │           │   │   │   ├── call_refer_params.py
    │           │   │   │   ├── call_reject_params.py
    │           │   │   │   ├── client_secret_create_params.py
    │           │   │   │   ├── client_secret_create_response.py
    │           │   │   │   ├── connect_client_event_param.py
    │           │   │   │   ├── conversation_created_event.py
    │           │   │   │   ├── conversation_item.py
    │           │   │   │   ├── conversation_item_added.py
    │           │   │   │   ├── conversation_item_create_event.py
    │           │   │   │   ├── conversation_item_create_event_param.py
    │           │   │   │   ├── conversation_item_created_event.py
    │           │   │   │   ├── conversation_item_delete_event.py
    │           │   │   │   ├── conversation_item_delete_event_param.py
    │           │   │   │   ├── conversation_item_deleted_event.py
    │           │   │   │   ├── conversation_item_done.py
    │           │   │   │   ├── conversation_item_input_audio_transcription_completed_event.py
    │           │   │   │   ├── conversation_item_input_audio_transcription_delta_event.py
    │           │   │   │   ├── conversation_item_input_audio_transcription_failed_event.py
    │           │   │   │   ├── conversation_item_input_audio_transcription_segment.py
    │           │   │   │   ├── conversation_item_param.py
    │           │   │   │   ├── conversation_item_retrieve_event.py
    │           │   │   │   ├── conversation_item_retrieve_event_param.py
    │           │   │   │   ├── conversation_item_truncate_event.py
    │           │   │   │   ├── conversation_item_truncate_event_param.py
    │           │   │   │   ├── conversation_item_truncated_event.py
    │           │   │   │   ├── input_audio_buffer_append_event.py
    │           │   │   │   ├── input_audio_buffer_append_event_param.py
    │           │   │   │   ├── input_audio_buffer_clear_event.py
    │           │   │   │   ├── input_audio_buffer_clear_event_param.py
    │           │   │   │   ├── input_audio_buffer_cleared_event.py
    │           │   │   │   ├── input_audio_buffer_commit_event.py
    │           │   │   │   ├── input_audio_buffer_commit_event_param.py
    │           │   │   │   ├── input_audio_buffer_committed_event.py
    │           │   │   │   ├── input_audio_buffer_dtmf_event_received_event.py
    │           │   │   │   ├── input_audio_buffer_speech_started_event.py
    │           │   │   │   ├── input_audio_buffer_speech_stopped_event.py
    │           │   │   │   ├── input_audio_buffer_timeout_triggered.py
    │           │   │   │   ├── log_prob_properties.py
    │           │   │   │   ├── mcp_list_tools_completed.py
    │           │   │   │   ├── mcp_list_tools_failed.py
    │           │   │   │   ├── mcp_list_tools_in_progress.py
    │           │   │   │   ├── noise_reduction_type.py
    │           │   │   │   ├── output_audio_buffer_clear_event.py
    │           │   │   │   ├── output_audio_buffer_clear_event_param.py
    │           │   │   │   ├── rate_limits_updated_event.py
    │           │   │   │   ├── realtime_audio_config.py
    │           │   │   │   ├── realtime_audio_config_input.py
    │           │   │   │   ├── realtime_audio_config_input_param.py
    │           │   │   │   ├── realtime_audio_config_output.py
    │           │   │   │   ├── realtime_audio_config_output_param.py
    │           │   │   │   ├── realtime_audio_config_param.py
    │           │   │   │   ├── realtime_audio_formats.py
    │           │   │   │   ├── realtime_audio_formats_param.py
    │           │   │   │   ├── realtime_audio_input_turn_detection.py
    │           │   │   │   ├── realtime_audio_input_turn_detection_param.py
    │           │   │   │   ├── realtime_client_event.py
    │           │   │   │   ├── realtime_client_event_param.py
    │           │   │   │   ├── realtime_connect_params.py
    │           │   │   │   ├── realtime_conversation_item_assistant_message.py
    │           │   │   │   ├── realtime_conversation_item_assistant_message_param.py
    │           │   │   │   ├── realtime_conversation_item_function_call.py
    │           │   │   │   ├── realtime_conversation_item_function_call_output.py
    │           │   │   │   ├── realtime_conversation_item_function_call_output_param.py
    │           │   │   │   ├── realtime_conversation_item_function_call_param.py
    │           │   │   │   ├── realtime_conversation_item_system_message.py
    │           │   │   │   ├── realtime_conversation_item_system_message_param.py
    │           │   │   │   ├── realtime_conversation_item_user_message.py
    │           │   │   │   ├── realtime_conversation_item_user_message_param.py
    │           │   │   │   ├── realtime_error.py
    │           │   │   │   ├── realtime_error_event.py
    │           │   │   │   ├── realtime_function_tool.py
    │           │   │   │   ├── realtime_function_tool_param.py
    │           │   │   │   ├── realtime_mcp_approval_request.py
    │           │   │   │   ├── realtime_mcp_approval_request_param.py
    │           │   │   │   ├── realtime_mcp_approval_response.py
    │           │   │   │   ├── realtime_mcp_approval_response_param.py
    │           │   │   │   ├── realtime_mcp_list_tools.py
    │           │   │   │   ├── realtime_mcp_list_tools_param.py
    │           │   │   │   ├── realtime_mcp_protocol_error.py
    │           │   │   │   ├── realtime_mcp_protocol_error_param.py
    │           │   │   │   ├── realtime_mcp_tool_call.py
    │           │   │   │   ├── realtime_mcp_tool_call_param.py
    │           │   │   │   ├── realtime_mcp_tool_execution_error.py
    │           │   │   │   ├── realtime_mcp_tool_execution_error_param.py
    │           │   │   │   ├── realtime_mcphttp_error.py
    │           │   │   │   ├── realtime_mcphttp_error_param.py
    │           │   │   │   ├── realtime_reasoning.py
    │           │   │   │   ├── realtime_reasoning_effort.py
    │           │   │   │   ├── realtime_reasoning_param.py
    │           │   │   │   ├── realtime_response.py
    │           │   │   │   ├── realtime_response_create_audio_output.py
    │           │   │   │   ├── realtime_response_create_audio_output_param.py
    │           │   │   │   ├── realtime_response_create_mcp_tool.py
    │           │   │   │   ├── realtime_response_create_mcp_tool_param.py
    │           │   │   │   ├── realtime_response_create_params.py
    │           │   │   │   ├── realtime_response_create_params_param.py
    │           │   │   │   ├── realtime_response_create_params_with_references_param.py
    │           │   │   │   ├── realtime_response_status.py
    │           │   │   │   ├── realtime_response_usage.py
    │           │   │   │   ├── realtime_response_usage_input_token_details.py
    │           │   │   │   ├── realtime_response_usage_output_token_details.py
    │           │   │   │   ├── realtime_server_event.py
    │           │   │   │   ├── realtime_session_create_request.py
    │           │   │   │   ├── realtime_session_create_request_param.py
    │           │   │   │   ├── realtime_session_create_response.py
    │           │   │   │   ├── realtime_tool_choice_config.py
    │           │   │   │   ├── realtime_tool_choice_config_param.py
    │           │   │   │   ├── realtime_tools_config.py
    │           │   │   │   ├── realtime_tools_config_param.py
    │           │   │   │   ├── realtime_tools_config_union.py
    │           │   │   │   ├── realtime_tools_config_union_param.py
    │           │   │   │   ├── realtime_tracing_config.py
    │           │   │   │   ├── realtime_tracing_config_param.py
    │           │   │   │   ├── realtime_transcription_session_audio.py
    │           │   │   │   ├── realtime_transcription_session_audio_input.py
    │           │   │   │   ├── realtime_transcription_session_audio_input_param.py
    │           │   │   │   ├── realtime_transcription_session_audio_input_turn_detection.py
    │           │   │   │   ├── realtime_transcription_session_audio_input_turn_detection_param.py
    │           │   │   │   ├── realtime_transcription_session_audio_param.py
    │           │   │   │   ├── realtime_transcription_session_create_request.py
    │           │   │   │   ├── realtime_transcription_session_create_request_param.py
    │           │   │   │   ├── realtime_transcription_session_create_response.py
    │           │   │   │   ├── realtime_transcription_session_turn_detection.py
    │           │   │   │   ├── realtime_translation_client_event.py
    │           │   │   │   ├── realtime_translation_client_event_param.py
    │           │   │   │   ├── realtime_translation_client_secret_create_response.py
    │           │   │   │   ├── realtime_translation_input_audio_buffer_append_event.py
    │           │   │   │   ├── realtime_translation_input_audio_buffer_append_event_param.py
    │           │   │   │   ├── realtime_translation_input_transcript_delta_event.py
    │           │   │   │   ├── realtime_translation_output_audio_delta_event.py
    │           │   │   │   ├── realtime_translation_output_transcript_delta_event.py
    │           │   │   │   ├── realtime_translation_server_event.py
    │           │   │   │   ├── realtime_translation_session.py
    │           │   │   │   ├── realtime_translation_session_close_event.py
    │           │   │   │   ├── realtime_translation_session_close_event_param.py
    │           │   │   │   ├── realtime_translation_session_closed_event.py
    │           │   │   │   ├── realtime_translation_session_create_request_param.py
    │           │   │   │   ├── realtime_translation_session_created_event.py
    │           │   │   │   ├── realtime_translation_session_update_event.py
    │           │   │   │   ├── realtime_translation_session_update_event_param.py
    │           │   │   │   ├── realtime_translation_session_update_request.py
    │           │   │   │   ├── realtime_translation_session_update_request_param.py
    │           │   │   │   ├── realtime_translation_session_updated_event.py
    │           │   │   │   ├── realtime_truncation.py
    │           │   │   │   ├── realtime_truncation_param.py
    │           │   │   │   ├── realtime_truncation_retention_ratio.py
    │           │   │   │   ├── realtime_truncation_retention_ratio_param.py
    │           │   │   │   ├── response_audio_delta_event.py
    │           │   │   │   ├── response_audio_done_event.py
    │           │   │   │   ├── response_audio_transcript_delta_event.py
    │           │   │   │   ├── response_audio_transcript_done_event.py
    │           │   │   │   ├── response_cancel_event.py
    │           │   │   │   ├── response_cancel_event_param.py
    │           │   │   │   ├── response_content_part_added_event.py
    │           │   │   │   ├── response_content_part_done_event.py
    │           │   │   │   ├── response_create_event.py
    │           │   │   │   ├── response_create_event_param.py
    │           │   │   │   ├── response_create_event_with_references_param.py
    │           │   │   │   ├── response_created_event.py
    │           │   │   │   ├── response_done_event.py
    │           │   │   │   ├── response_function_call_arguments_delta_event.py
    │           │   │   │   ├── response_function_call_arguments_done_event.py
    │           │   │   │   ├── response_item_reference.py
    │           │   │   │   ├── response_item_reference_param.py
    │           │   │   │   ├── response_mcp_call_arguments_delta.py
    │           │   │   │   ├── response_mcp_call_arguments_done.py
    │           │   │   │   ├── response_mcp_call_completed.py
    │           │   │   │   ├── response_mcp_call_failed.py
    │           │   │   │   ├── response_mcp_call_in_progress.py
    │           │   │   │   ├── response_output_item_added_event.py
    │           │   │   │   ├── response_output_item_done_event.py
    │           │   │   │   ├── response_text_delta_event.py
    │           │   │   │   ├── response_text_done_event.py
    │           │   │   │   ├── session_created_event.py
    │           │   │   │   ├── session_update_event.py
    │           │   │   │   ├── session_update_event_param.py
    │           │   │   │   ├── session_updated_event.py
    │           │   │   │   └── translations
    │           │   │   │       ├── __init__.py
    │           │   │   │       └── client_secret_create_params.py
    │           │   │   ├── responses
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── apply_patch_tool.py
    │           │   │   │   ├── apply_patch_tool_param.py
    │           │   │   │   ├── compacted_response.py
    │           │   │   │   ├── computer_action.py
    │           │   │   │   ├── computer_action_list.py
    │           │   │   │   ├── computer_action_list_param.py
    │           │   │   │   ├── computer_action_param.py
    │           │   │   │   ├── computer_tool.py
    │           │   │   │   ├── computer_tool_param.py
    │           │   │   │   ├── computer_use_preview_tool.py
    │           │   │   │   ├── computer_use_preview_tool_param.py
    │           │   │   │   ├── container_auto.py
    │           │   │   │   ├── container_auto_param.py
    │           │   │   │   ├── container_network_policy_allowlist.py
    │           │   │   │   ├── container_network_policy_allowlist_param.py
    │           │   │   │   ├── container_network_policy_disabled.py
    │           │   │   │   ├── container_network_policy_disabled_param.py
    │           │   │   │   ├── container_network_policy_domain_secret.py
    │           │   │   │   ├── container_network_policy_domain_secret_param.py
    │           │   │   │   ├── container_reference.py
    │           │   │   │   ├── container_reference_param.py
    │           │   │   │   ├── custom_tool.py
    │           │   │   │   ├── custom_tool_param.py
    │           │   │   │   ├── easy_input_message.py
    │           │   │   │   ├── easy_input_message_param.py
    │           │   │   │   ├── file_search_tool.py
    │           │   │   │   ├── file_search_tool_param.py
    │           │   │   │   ├── function_shell_tool.py
    │           │   │   │   ├── function_shell_tool_param.py
    │           │   │   │   ├── function_tool.py
    │           │   │   │   ├── function_tool_param.py
    │           │   │   │   ├── image_detail.py
    │           │   │   │   ├── inline_skill.py
    │           │   │   │   ├── inline_skill_param.py
    │           │   │   │   ├── inline_skill_source.py
    │           │   │   │   ├── inline_skill_source_param.py
    │           │   │   │   ├── input_item_list_params.py
    │           │   │   │   ├── input_token_count_params.py
    │           │   │   │   ├── input_token_count_response.py
    │           │   │   │   ├── local_environment.py
    │           │   │   │   ├── local_environment_param.py
    │           │   │   │   ├── local_skill.py
    │           │   │   │   ├── local_skill_param.py
    │           │   │   │   ├── mcp_tool_call_error.py
    │           │   │   │   ├── mcp_tool_call_error_param.py
    │           │   │   │   ├── namespace_tool.py
    │           │   │   │   ├── namespace_tool_param.py
    │           │   │   │   ├── parsed_response.py
    │           │   │   │   ├── response.py
    │           │   │   │   ├── response_apply_patch_tool_call.py
    │           │   │   │   ├── response_apply_patch_tool_call_output.py
    │           │   │   │   ├── response_audio_delta_event.py
    │           │   │   │   ├── response_audio_done_event.py
    │           │   │   │   ├── response_audio_transcript_delta_event.py
    │           │   │   │   ├── response_audio_transcript_done_event.py
    │           │   │   │   ├── response_code_interpreter_call_code_delta_event.py
    │           │   │   │   ├── response_code_interpreter_call_code_done_event.py
    │           │   │   │   ├── response_code_interpreter_call_completed_event.py
    │           │   │   │   ├── response_code_interpreter_call_in_progress_event.py
    │           │   │   │   ├── response_code_interpreter_call_interpreting_event.py
    │           │   │   │   ├── response_code_interpreter_tool_call.py
    │           │   │   │   ├── response_code_interpreter_tool_call_param.py
    │           │   │   │   ├── response_compact_params.py
    │           │   │   │   ├── response_compaction_compacting_event.py
    │           │   │   │   ├── response_compaction_item.py
    │           │   │   │   ├── response_compaction_item_param.py
    │           │   │   │   ├── response_compaction_item_param_param.py
    │           │   │   │   ├── response_completed_event.py
    │           │   │   │   ├── response_computer_tool_call.py
    │           │   │   │   ├── response_computer_tool_call_output_item.py
    │           │   │   │   ├── response_computer_tool_call_output_screenshot.py
    │           │   │   │   ├── response_computer_tool_call_output_screenshot_param.py
    │           │   │   │   ├── response_computer_tool_call_param.py
    │           │   │   │   ├── response_configuration_update_item.py
    │           │   │   │   ├── response_configuration_update_item_param.py
    │           │   │   │   ├── response_configuration_update_item_param_param.py
    │           │   │   │   ├── response_container_reference.py
    │           │   │   │   ├── response_content_part_added_event.py
    │           │   │   │   ├── response_content_part_done_event.py
    │           │   │   │   ├── response_conversation_param.py
    │           │   │   │   ├── response_conversation_param_param.py
    │           │   │   │   ├── response_create_params.py
    │           │   │   │   ├── response_created_event.py
    │           │   │   │   ├── response_custom_tool_call.py
    │           │   │   │   ├── response_custom_tool_call_input_delta_event.py
    │           │   │   │   ├── response_custom_tool_call_input_done_event.py
    │           │   │   │   ├── response_custom_tool_call_item.py
    │           │   │   │   ├── response_custom_tool_call_output.py
    │           │   │   │   ├── response_custom_tool_call_output_item.py
    │           │   │   │   ├── response_custom_tool_call_output_param.py
    │           │   │   │   ├── response_custom_tool_call_param.py
    │           │   │   │   ├── response_error.py
    │           │   │   │   ├── response_error_event.py
    │           │   │   │   ├── response_failed_event.py
    │           │   │   │   ├── response_file_search_call_completed_event.py
    │           │   │   │   ├── response_file_search_call_in_progress_event.py
    │           │   │   │   ├── response_file_search_call_searching_event.py
    │           │   │   │   ├── response_file_search_tool_call.py
    │           │   │   │   ├── response_file_search_tool_call_param.py
    │           │   │   │   ├── response_format_text_config.py
    │           │   │   │   ├── response_format_text_config_param.py
    │           │   │   │   ├── response_format_text_json_schema_config.py
    │           │   │   │   ├── response_format_text_json_schema_config_param.py
    │           │   │   │   ├── response_function_call_arguments_delta_event.py
    │           │   │   │   ├── response_function_call_arguments_done_event.py
    │           │   │   │   ├── response_function_call_output_item.py
    │           │   │   │   ├── response_function_call_output_item_list.py
    │           │   │   │   ├── response_function_call_output_item_list_param.py
    │           │   │   │   ├── response_function_call_output_item_param.py
    │           │   │   │   ├── response_function_shell_call_output_content.py
    │           │   │   │   ├── response_function_shell_call_output_content_param.py
    │           │   │   │   ├── response_function_shell_tool_call.py
    │           │   │   │   ├── response_function_shell_tool_call_output.py
    │           │   │   │   ├── response_function_tool_call.py
    │           │   │   │   ├── response_function_tool_call_item.py
    │           │   │   │   ├── response_function_tool_call_output_item.py
    │           │   │   │   ├── response_function_tool_call_param.py
    │           │   │   │   ├── response_function_web_search.py
    │           │   │   │   ├── response_function_web_search_param.py
    │           │   │   │   ├── response_image_gen_call_completed_event.py
    │           │   │   │   ├── response_image_gen_call_generating_event.py
    │           │   │   │   ├── response_image_gen_call_in_progress_event.py
    │           │   │   │   ├── response_image_gen_call_partial_image_event.py
    │           │   │   │   ├── response_in_progress_event.py
    │           │   │   │   ├── response_includable.py
    │           │   │   │   ├── response_incomplete_event.py
    │           │   │   │   ├── response_input.py
    │           │   │   │   ├── response_input_audio.py
    │           │   │   │   ├── response_input_audio_param.py
    │           │   │   │   ├── response_input_content.py
    │           │   │   │   ├── response_input_content_param.py
    │           │   │   │   ├── response_input_file.py
    │           │   │   │   ├── response_input_file_content.py
    │           │   │   │   ├── response_input_file_content_param.py
    │           │   │   │   ├── response_input_file_param.py
    │           │   │   │   ├── response_input_image.py
    │           │   │   │   ├── response_input_image_content.py
    │           │   │   │   ├── response_input_image_content_param.py
    │           │   │   │   ├── response_input_image_param.py
    │           │   │   │   ├── response_input_item.py
    │           │   │   │   ├── response_input_item_param.py
    │           │   │   │   ├── response_input_message_content_list.py
    │           │   │   │   ├── response_input_message_content_list_param.py
    │           │   │   │   ├── response_input_message_item.py
    │           │   │   │   ├── response_input_param.py
    │           │   │   │   ├── response_input_text.py
    │           │   │   │   ├── response_input_text_content.py
    │           │   │   │   ├── response_input_text_content_param.py
    │           │   │   │   ├── response_input_text_param.py
    │           │   │   │   ├── response_item.py
    │           │   │   │   ├── response_item_list.py
    │           │   │   │   ├── response_local_environment.py
    │           │   │   │   ├── response_mcp_call_arguments_delta_event.py
    │           │   │   │   ├── response_mcp_call_arguments_done_event.py
    │           │   │   │   ├── response_mcp_call_completed_event.py
    │           │   │   │   ├── response_mcp_call_failed_event.py
    │           │   │   │   ├── response_mcp_call_in_progress_event.py
    │           │   │   │   ├── response_mcp_list_tools_completed_event.py
    │           │   │   │   ├── response_mcp_list_tools_failed_event.py
    │           │   │   │   ├── response_mcp_list_tools_in_progress_event.py
    │           │   │   │   ├── response_output_item.py
    │           │   │   │   ├── response_output_item_added_event.py
    │           │   │   │   ├── response_output_item_done_event.py
    │           │   │   │   ├── response_output_message.py
    │           │   │   │   ├── response_output_message_param.py
    │           │   │   │   ├── response_output_refusal.py
    │           │   │   │   ├── response_output_refusal_param.py
    │           │   │   │   ├── response_output_text.py
    │           │   │   │   ├── response_output_text_annotation_added_event.py
    │           │   │   │   ├── response_output_text_param.py
    │           │   │   │   ├── response_prompt.py
    │           │   │   │   ├── response_prompt_param.py
    │           │   │   │   ├── response_queued_event.py
    │           │   │   │   ├── response_reasoning_item.py
    │           │   │   │   ├── response_reasoning_item_param.py
    │           │   │   │   ├── response_reasoning_summary_part_added_event.py
    │           │   │   │   ├── response_reasoning_summary_part_done_event.py
    │           │   │   │   ├── response_reasoning_summary_text_delta_event.py
    │           │   │   │   ├── response_reasoning_summary_text_done_event.py
    │           │   │   │   ├── response_reasoning_text_delta_event.py
    │           │   │   │   ├── response_reasoning_text_done_event.py
    │           │   │   │   ├── response_refusal_delta_event.py
    │           │   │   │   ├── response_refusal_done_event.py
    │           │   │   │   ├── response_retrieve_params.py
    │           │   │   │   ├── response_shell_call_command_added_event.py
    │           │   │   │   ├── response_shell_call_command_delta_event.py
    │           │   │   │   ├── response_shell_call_command_done_event.py
    │           │   │   │   ├── response_shell_call_output_content_delta_event.py
    │           │   │   │   ├── response_shell_call_output_content_done_event.py
    │           │   │   │   ├── response_status.py
    │           │   │   │   ├── response_steer_accepted_event.py
    │           │   │   │   ├── response_steer_error_code.py
    │           │   │   │   ├── response_steer_event.py
    │           │   │   │   ├── response_steer_event_param.py
    │           │   │   │   ├── response_steer_failed_event.py
    │           │   │   │   ├── response_steer_input.py
    │           │   │   │   ├── response_steer_input_content.py
    │           │   │   │   ├── response_steer_input_content_param.py
    │           │   │   │   ├── response_steer_input_param.py
    │           │   │   │   ├── response_steer_pending_event.py
    │           │   │   │   ├── response_steer_pending_reason.py
    │           │   │   │   ├── response_steer_required_input.py
    │           │   │   │   ├── response_stream_event.py
    │           │   │   │   ├── response_text_config.py
    │           │   │   │   ├── response_text_config_param.py
    │           │   │   │   ├── response_text_delta_event.py
    │           │   │   │   ├── response_text_done_event.py
    │           │   │   │   ├── response_tool_search_call.py
    │           │   │   │   ├── response_tool_search_output_item.py
    │           │   │   │   ├── response_tool_search_output_item_param.py
    │           │   │   │   ├── response_tool_search_output_item_param_param.py
    │           │   │   │   ├── response_usage.py
    │           │   │   │   ├── response_web_search_call_completed_event.py
    │           │   │   │   ├── response_web_search_call_in_progress_event.py
    │           │   │   │   ├── response_web_search_call_searching_event.py
    │           │   │   │   ├── responses_client_event.py
    │           │   │   │   ├── responses_client_event_param.py
    │           │   │   │   ├── responses_server_event.py
    │           │   │   │   ├── service_tier.py
    │           │   │   │   ├── skill_reference.py
    │           │   │   │   ├── skill_reference_param.py
    │           │   │   │   ├── tool.py
    │           │   │   │   ├── tool_choice_allowed.py
    │           │   │   │   ├── tool_choice_allowed_param.py
    │           │   │   │   ├── tool_choice_apply_patch.py
    │           │   │   │   ├── tool_choice_apply_patch_param.py
    │           │   │   │   ├── tool_choice_custom.py
    │           │   │   │   ├── tool_choice_custom_param.py
    │           │   │   │   ├── tool_choice_function.py
    │           │   │   │   ├── tool_choice_function_param.py
    │           │   │   │   ├── tool_choice_mcp.py
    │           │   │   │   ├── tool_choice_mcp_param.py
    │           │   │   │   ├── tool_choice_options.py
    │           │   │   │   ├── tool_choice_shell.py
    │           │   │   │   ├── tool_choice_shell_param.py
    │           │   │   │   ├── tool_choice_types.py
    │           │   │   │   ├── tool_choice_types_param.py
    │           │   │   │   ├── tool_param.py
    │           │   │   │   ├── tool_search_output_namespace_tool.py
    │           │   │   │   ├── tool_search_output_namespace_tool_param.py
    │           │   │   │   ├── tool_search_tool.py
    │           │   │   │   ├── tool_search_tool_param.py
    │           │   │   │   ├── web_search_preview_tool.py
    │           │   │   │   ├── web_search_preview_tool_param.py
    │           │   │   │   ├── web_search_tool.py
    │           │   │   │   └── web_search_tool_param.py
    │           │   │   ├── safety
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── safety_alert.py
    │           │   │   │   └── safety_case.py
    │           │   │   ├── shared
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── all_models.py
    │           │   │   │   ├── chat_model.py
    │           │   │   │   ├── comparison_filter.py
    │           │   │   │   ├── compound_filter.py
    │           │   │   │   ├── custom_tool_input_format.py
    │           │   │   │   ├── decision_input_json.py
    │           │   │   │   ├── decision_question_input_image.py
    │           │   │   │   ├── decision_question_input_part.py
    │           │   │   │   ├── decision_question_input_text.py
    │           │   │   │   ├── error_object.py
    │           │   │   │   ├── function_definition.py
    │           │   │   │   ├── function_parameters.py
    │           │   │   │   ├── metadata.py
    │           │   │   │   ├── oauth_error_code.py
    │           │   │   │   ├── reasoning.py
    │           │   │   │   ├── reasoning_effort.py
    │           │   │   │   ├── response_format_json_object.py
    │           │   │   │   ├── response_format_json_schema.py
    │           │   │   │   ├── response_format_text.py
    │           │   │   │   ├── response_format_text_grammar.py
    │           │   │   │   ├── response_format_text_python.py
    │           │   │   │   └── responses_model.py
    │           │   │   ├── shared_params
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── chat_model.py
    │           │   │   │   ├── comparison_filter.py
    │           │   │   │   ├── compound_filter.py
    │           │   │   │   ├── custom_tool_input_format.py
    │           │   │   │   ├── decision_input_json.py
    │           │   │   │   ├── decision_question_input_image.py
    │           │   │   │   ├── decision_question_input_part.py
    │           │   │   │   ├── decision_question_input_text.py
    │           │   │   │   ├── function_definition.py
    │           │   │   │   ├── function_parameters.py
    │           │   │   │   ├── metadata.py
    │           │   │   │   ├── oauth_error_code.py
    │           │   │   │   ├── reasoning.py
    │           │   │   │   ├── reasoning_effort.py
    │           │   │   │   ├── response_format_json_object.py
    │           │   │   │   ├── response_format_json_schema.py
    │           │   │   │   ├── response_format_text.py
    │           │   │   │   └── responses_model.py
    │           │   │   ├── skill.py
    │           │   │   ├── skill_create_params.py
    │           │   │   ├── skill_list.py
    │           │   │   ├── skill_list_params.py
    │           │   │   ├── skill_update_params.py
    │           │   │   ├── skills
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── deleted_skill_version.py
    │           │   │   │   ├── skill_version.py
    │           │   │   │   ├── skill_version_list.py
    │           │   │   │   ├── version_create_params.py
    │           │   │   │   ├── version_list_params.py
    │           │   │   │   └── versions
    │           │   │   │       └── __init__.py
    │           │   │   ├── static_file_chunking_strategy.py
    │           │   │   ├── static_file_chunking_strategy_object.py
    │           │   │   ├── static_file_chunking_strategy_object_param.py
    │           │   │   ├── static_file_chunking_strategy_param.py
    │           │   │   ├── upload.py
    │           │   │   ├── upload_complete_params.py
    │           │   │   ├── upload_create_params.py
    │           │   │   ├── uploads
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── part_create_params.py
    │           │   │   │   └── upload_part.py
    │           │   │   ├── vector_store.py
    │           │   │   ├── vector_store_create_params.py
    │           │   │   ├── vector_store_deleted.py
    │           │   │   ├── vector_store_list_params.py
    │           │   │   ├── vector_store_search_params.py
    │           │   │   ├── vector_store_search_response.py
    │           │   │   ├── vector_store_update_params.py
    │           │   │   ├── vector_stores
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── file_batch_create_params.py
    │           │   │   │   ├── file_batch_list_files_params.py
    │           │   │   │   ├── file_content_response.py
    │           │   │   │   ├── file_create_params.py
    │           │   │   │   ├── file_list_params.py
    │           │   │   │   ├── file_update_params.py
    │           │   │   │   ├── vector_store_file.py
    │           │   │   │   ├── vector_store_file_batch.py
    │           │   │   │   └── vector_store_file_deleted.py
    │           │   │   ├── video.py
    │           │   │   ├── video_create_character_params.py
    │           │   │   ├── video_create_character_response.py
    │           │   │   ├── video_create_error.py
    │           │   │   ├── video_create_params.py
    │           │   │   ├── video_delete_response.py
    │           │   │   ├── video_download_content_params.py
    │           │   │   ├── video_edit_params.py
    │           │   │   ├── video_extend_params.py
    │           │   │   ├── video_get_character_response.py
    │           │   │   ├── video_list_params.py
    │           │   │   ├── video_model.py
    │           │   │   ├── video_model_param.py
    │           │   │   ├── video_remix_params.py
    │           │   │   ├── video_seconds.py
    │           │   │   ├── video_size.py
    │           │   │   ├── webhooks
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── agent_environment_expired_webhook_event.py
    │           │   │   │   ├── agent_environment_failed_webhook_event.py
    │           │   │   │   ├── agent_environment_ready_webhook_event.py
    │           │   │   │   ├── agent_environment_suspended_webhook_event.py
    │           │   │   │   ├── agent_session_action_required_webhook_event.py
    │           │   │   │   ├── agent_session_created_webhook_event.py
    │           │   │   │   ├── agent_session_failed_webhook_event.py
    │           │   │   │   ├── agent_session_idle_webhook_event.py
    │           │   │   │   ├── agent_session_in_progress_webhook_event.py
    │           │   │   │   ├── batch_cancelled_webhook_event.py
    │           │   │   │   ├── batch_completed_webhook_event.py
    │           │   │   │   ├── batch_expired_webhook_event.py
    │           │   │   │   ├── batch_failed_webhook_event.py
    │           │   │   │   ├── deleted_webhook_endpoint.py
    │           │   │   │   ├── eval_run_canceled_webhook_event.py
    │           │   │   │   ├── eval_run_failed_webhook_event.py
    │           │   │   │   ├── eval_run_succeeded_webhook_event.py
    │           │   │   │   ├── fine_tuning_job_cancelled_webhook_event.py
    │           │   │   │   ├── fine_tuning_job_failed_webhook_event.py
    │           │   │   │   ├── fine_tuning_job_succeeded_webhook_event.py
    │           │   │   │   ├── live_call_incoming_webhook_event.py
    │           │   │   │   ├── live_transport_connected_webhook_event.py
    │           │   │   │   ├── live_transport_incoming_webhook_event.py
    │           │   │   │   ├── realtime_call_incoming_webhook_event.py
    │           │   │   │   ├── response_cancelled_webhook_event.py
    │           │   │   │   ├── response_completed_webhook_event.py
    │           │   │   │   ├── response_failed_webhook_event.py
    │           │   │   │   ├── response_incomplete_webhook_event.py
    │           │   │   │   ├── safety_alert_created_webhook_event.py
    │           │   │   │   ├── safety_deactivation_issued_webhook_event.py
    │           │   │   │   ├── safety_identifier_blocked_webhook_event.py
    │           │   │   │   ├── safety_org_alert_created_webhook_event.py
    │           │   │   │   ├── safety_warning_issued_webhook_event.py
    │           │   │   │   ├── unwrap_webhook_event.py
    │           │   │   │   ├── webhook_create_params.py
    │           │   │   │   ├── webhook_endpoint.py
    │           │   │   │   ├── webhook_endpoint_list.py
    │           │   │   │   ├── webhook_endpoint_test_result.py
    │           │   │   │   ├── webhook_endpoint_with_secret.py
    │           │   │   │   ├── webhook_event_type_list.py
    │           │   │   │   ├── webhook_list_params.py
    │           │   │   │   ├── webhook_rotate_secret_params.py
    │           │   │   │   ├── webhook_test_params.py
    │           │   │   │   └── webhook_update_params.py
    │           │   │   ├── websocket_connection_options.py
    │           │   │   └── websocket_reconnection.py
    │           │   └── version.py
    │           ├── openai-3.51.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── opencv_python_headless-5.0.0.93.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE-3RD-PARTY.txt
    │           │   ├── LICENSE.txt
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── sboms
    │           │   │   └── auditwheel.cdx.json
    │           │   └── top_level.txt
    │           ├── opencv_python_headless.libs
    │           │   ├── libaom-a0d22147.so.3.14.1
    │           │   ├── libavcodec-c4204469.so.62.28.101
    │           │   ├── libavformat-4762a711.so.62.12.101
    │           │   ├── libavif-43e630fc.so.16.4.2
    │           │   ├── libavutil-befbbc48.so.60.26.101
    │           │   ├── libcrypto-5409cd36.so.1.1.1k
    │           │   ├── libdrm-b0291a67.so.2.4.0
    │           │   ├── libgfortran-83c28eba.so.5.0.0
    │           │   ├── libopenblasp-r0-59ffcd50.3.15.so
    │           │   ├── libpng16-529cb57a.so.16.58.0
    │           │   ├── libquadmath-2284e583.so.0.0.0
    │           │   ├── libssl-81259c47.so.1.1.1k
    │           │   ├── libswresample-2dfded3b.so.6.3.101
    │           │   ├── libswscale-fe215b0b.so.9.5.101
    │           │   └── libvpx-4fb239ff.so.11.0.1
    │           ├── openpyxl
    │           │   ├── __init__.py
    │           │   ├── _constants.py
    │           │   ├── cell
    │           │   │   ├── __init__.py
    │           │   │   ├── _writer.py
    │           │   │   ├── cell.py
    │           │   │   ├── read_only.py
    │           │   │   ├── rich_text.py
    │           │   │   └── text.py
    │           │   ├── chart
    │           │   │   ├── _3d.py
    │           │   │   ├── __init__.py
    │           │   │   ├── _chart.py
    │           │   │   ├── area_chart.py
    │           │   │   ├── axis.py
    │           │   │   ├── bar_chart.py
    │           │   │   ├── bubble_chart.py
    │           │   │   ├── chartspace.py
    │           │   │   ├── data_source.py
    │           │   │   ├── descriptors.py
    │           │   │   ├── error_bar.py
    │           │   │   ├── label.py
    │           │   │   ├── layout.py
    │           │   │   ├── legend.py
    │           │   │   ├── line_chart.py
    │           │   │   ├── marker.py
    │           │   │   ├── picture.py
    │           │   │   ├── pie_chart.py
    │           │   │   ├── pivot.py
    │           │   │   ├── plotarea.py
    │           │   │   ├── print_settings.py
    │           │   │   ├── radar_chart.py
    │           │   │   ├── reader.py
    │           │   │   ├── reference.py
    │           │   │   ├── scatter_chart.py
    │           │   │   ├── series.py
    │           │   │   ├── series_factory.py
    │           │   │   ├── shapes.py
    │           │   │   ├── stock_chart.py
    │           │   │   ├── surface_chart.py
    │           │   │   ├── text.py
    │           │   │   ├── title.py
    │           │   │   ├── trendline.py
    │           │   │   └── updown_bars.py
    │           │   ├── chartsheet
    │           │   │   ├── __init__.py
    │           │   │   ├── chartsheet.py
    │           │   │   ├── custom.py
    │           │   │   ├── properties.py
    │           │   │   ├── protection.py
    │           │   │   ├── publish.py
    │           │   │   ├── relation.py
    │           │   │   └── views.py
    │           │   ├── comments
    │           │   │   ├── __init__.py
    │           │   │   ├── author.py
    │           │   │   ├── comment_sheet.py
    │           │   │   ├── comments.py
    │           │   │   └── shape_writer.py
    │           │   ├── compat
    │           │   │   ├── __init__.py
    │           │   │   ├── abc.py
    │           │   │   ├── numbers.py
    │           │   │   ├── product.py
    │           │   │   ├── singleton.py
    │           │   │   └── strings.py
    │           │   ├── descriptors
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── container.py
    │           │   │   ├── excel.py
    │           │   │   ├── namespace.py
    │           │   │   ├── nested.py
    │           │   │   ├── sequence.py
    │           │   │   ├── serialisable.py
    │           │   │   └── slots.py
    │           │   ├── drawing
    │           │   │   ├── __init__.py
    │           │   │   ├── colors.py
    │           │   │   ├── connector.py
    │           │   │   ├── drawing.py
    │           │   │   ├── effect.py
    │           │   │   ├── fill.py
    │           │   │   ├── geometry.py
    │           │   │   ├── graphic.py
    │           │   │   ├── image.py
    │           │   │   ├── line.py
    │           │   │   ├── picture.py
    │           │   │   ├── properties.py
    │           │   │   ├── relation.py
    │           │   │   ├── spreadsheet_drawing.py
    │           │   │   ├── text.py
    │           │   │   └── xdr.py
    │           │   ├── formatting
    │           │   │   ├── __init__.py
    │           │   │   ├── formatting.py
    │           │   │   └── rule.py
    │           │   ├── formula
    │           │   │   ├── __init__.py
    │           │   │   ├── tokenizer.py
    │           │   │   └── translate.py
    │           │   ├── packaging
    │           │   │   ├── __init__.py
    │           │   │   ├── core.py
    │           │   │   ├── custom.py
    │           │   │   ├── extended.py
    │           │   │   ├── interface.py
    │           │   │   ├── manifest.py
    │           │   │   ├── relationship.py
    │           │   │   └── workbook.py
    │           │   ├── pivot
    │           │   │   ├── __init__.py
    │           │   │   ├── cache.py
    │           │   │   ├── fields.py
    │           │   │   ├── record.py
    │           │   │   └── table.py
    │           │   ├── reader
    │           │   │   ├── __init__.py
    │           │   │   ├── drawings.py
    │           │   │   ├── excel.py
    │           │   │   ├── strings.py
    │           │   │   └── workbook.py
    │           │   ├── styles
    │           │   │   ├── __init__.py
    │           │   │   ├── alignment.py
    │           │   │   ├── borders.py
    │           │   │   ├── builtins.py
    │           │   │   ├── cell_style.py
    │           │   │   ├── colors.py
    │           │   │   ├── differential.py
    │           │   │   ├── fills.py
    │           │   │   ├── fonts.py
    │           │   │   ├── named_styles.py
    │           │   │   ├── numbers.py
    │           │   │   ├── protection.py
    │           │   │   ├── proxy.py
    │           │   │   ├── styleable.py
    │           │   │   ├── stylesheet.py
    │           │   │   └── table.py
    │           │   ├── utils
    │           │   │   ├── __init__.py
    │           │   │   ├── bound_dictionary.py
    │           │   │   ├── cell.py
    │           │   │   ├── dataframe.py
    │           │   │   ├── datetime.py
    │           │   │   ├── escape.py
    │           │   │   ├── exceptions.py
    │           │   │   ├── formulas.py
    │           │   │   ├── indexed_list.py
    │           │   │   ├── inference.py
    │           │   │   ├── protection.py
    │           │   │   └── units.py
    │           │   ├── workbook
    │           │   │   ├── __init__.py
    │           │   │   ├── _writer.py
    │           │   │   ├── child.py
    │           │   │   ├── defined_name.py
    │           │   │   ├── external_link
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── external.py
    │           │   │   ├── external_reference.py
    │           │   │   ├── function_group.py
    │           │   │   ├── properties.py
    │           │   │   ├── protection.py
    │           │   │   ├── smart_tags.py
    │           │   │   ├── views.py
    │           │   │   ├── web.py
    │           │   │   └── workbook.py
    │           │   ├── worksheet
    │           │   │   ├── __init__.py
    │           │   │   ├── _read_only.py
    │           │   │   ├── _reader.py
    │           │   │   ├── _write_only.py
    │           │   │   ├── _writer.py
    │           │   │   ├── cell_range.py
    │           │   │   ├── cell_watch.py
    │           │   │   ├── controls.py
    │           │   │   ├── copier.py
    │           │   │   ├── custom.py
    │           │   │   ├── datavalidation.py
    │           │   │   ├── dimensions.py
    │           │   │   ├── drawing.py
    │           │   │   ├── errors.py
    │           │   │   ├── filters.py
    │           │   │   ├── formula.py
    │           │   │   ├── header_footer.py
    │           │   │   ├── hyperlink.py
    │           │   │   ├── merge.py
    │           │   │   ├── ole.py
    │           │   │   ├── page.py
    │           │   │   ├── pagebreak.py
    │           │   │   ├── picture.py
    │           │   │   ├── print_settings.py
    │           │   │   ├── properties.py
    │           │   │   ├── protection.py
    │           │   │   ├── related.py
    │           │   │   ├── scenario.py
    │           │   │   ├── smart_tag.py
    │           │   │   ├── table.py
    │           │   │   ├── views.py
    │           │   │   └── worksheet.py
    │           │   ├── writer
    │           │   │   ├── __init__.py
    │           │   │   ├── excel.py
    │           │   │   └── theme.py
    │           │   └── xml
    │           │       ├── __init__.py
    │           │       ├── constants.py
    │           │       └── functions.py
    │           ├── openpyxl-3.1.5.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENCE.rst
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── opentelemetry
    │           │   ├── _logs
    │           │   │   ├── __init__.py
    │           │   │   ├── _internal
    │           │   │   │   └── __init__.py
    │           │   │   ├── py.typed
    │           │   │   └── severity
    │           │   │       └── __init__.py
    │           │   ├── attributes
    │           │   │   ├── __init__.py
    │           │   │   └── py.typed
    │           │   ├── baggage
    │           │   │   ├── __init__.py
    │           │   │   ├── propagation
    │           │   │   │   └── __init__.py
    │           │   │   └── py.typed
    │           │   ├── context
    │           │   │   ├── __init__.py
    │           │   │   ├── context.py
    │           │   │   ├── contextvars_context.py
    │           │   │   └── py.typed
    │           │   ├── environment_variables
    │           │   │   ├── __init__.py
    │           │   │   └── py.typed
    │           │   ├── metrics
    │           │   │   ├── __init__.py
    │           │   │   ├── _internal
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── instrument.py
    │           │   │   │   └── observation.py
    │           │   │   └── py.typed
    │           │   ├── propagate
    │           │   │   ├── __init__.py
    │           │   │   └── py.typed
    │           │   ├── propagators
    │           │   │   ├── _envcarrier.py
    │           │   │   ├── composite.py
    │           │   │   ├── py.typed
    │           │   │   └── textmap.py
    │           │   ├── py.typed
    │           │   ├── trace
    │           │   │   ├── __init__.py
    │           │   │   ├── propagation
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── tracecontext.py
    │           │   │   ├── py.typed
    │           │   │   ├── span.py
    │           │   │   └── status.py
    │           │   ├── util
    │           │   │   ├── _decorator.py
    │           │   │   ├── _importlib_metadata.py
    │           │   │   ├── _once.py
    │           │   │   ├── _providers.py
    │           │   │   ├── py.typed
    │           │   │   ├── re.py
    │           │   │   └── types.py
    │           │   └── version
    │           │       ├── __init__.py
    │           │       └── py.typed
    │           ├── opentelemetry_api-1.45.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── packaging
    │           │   ├── __init__.py
    │           │   ├── _elffile.py
    │           │   ├── _manylinux.py
    │           │   ├── _musllinux.py
    │           │   ├── _parser.py
    │           │   ├── _ranges.py
    │           │   ├── _structures.py
    │           │   ├── _tokenizer.py
    │           │   ├── dependency_groups.py
    │           │   ├── direct_url.py
    │           │   ├── errors.py
    │           │   ├── licenses
    │           │   │   ├── __init__.py
    │           │   │   └── _spdx.py
    │           │   ├── markers.py
    │           │   ├── metadata.py
    │           │   ├── py.typed
    │           │   ├── pylock.py
    │           │   ├── ranges.py
    │           │   ├── requirements.py
    │           │   ├── specifiers.py
    │           │   ├── tags.py
    │           │   ├── utils.py
    │           │   └── version.py
    │           ├── packaging-26.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       ├── LICENSE
    │           │       ├── LICENSE.APACHE
    │           │       └── LICENSE.BSD
    │           ├── pandas
    │           │   ├── __init__.py
    │           │   ├── _config
    │           │   │   ├── __init__.py
    │           │   │   ├── config.py
    │           │   │   ├── dates.py
    │           │   │   ├── display.py
    │           │   │   └── localization.py
    │           │   ├── _libs
    │           │   │   ├── __init__.py
    │           │   │   ├── _cyutility.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _ujson.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _ujson.pyi
    │           │   │   ├── algos.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── algos.pyi
    │           │   │   ├── arrays.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── arrays.pyi
    │           │   │   ├── byteswap.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── byteswap.pyi
    │           │   │   ├── groupby.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── groupby.pyi
    │           │   │   ├── hashing.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── hashing.pyi
    │           │   │   ├── hashtable.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── hashtable.pyi
    │           │   │   ├── index.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── index.pyi
    │           │   │   ├── indexing.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── indexing.pyi
    │           │   │   ├── internals.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── internals.pyi
    │           │   │   ├── interval.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── interval.pyi
    │           │   │   ├── join.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── join.pyi
    │           │   │   ├── lib.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── lib.pyi
    │           │   │   ├── missing.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── missing.pyi
    │           │   │   ├── ops.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── ops.pyi
    │           │   │   ├── ops_dispatch.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── ops_dispatch.pyi
    │           │   │   ├── pandas_datetime.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── pandas_parser.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── parsers.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── parsers.pyi
    │           │   │   ├── properties.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── properties.pyi
    │           │   │   ├── reshape.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── reshape.pyi
    │           │   │   ├── sas.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── sas.pyi
    │           │   │   ├── sparse.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── sparse.pyi
    │           │   │   ├── testing.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── testing.pyi
    │           │   │   ├── tslib.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── tslib.pyi
    │           │   │   ├── tslibs
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── ccalendar.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── ccalendar.pyi
    │           │   │   │   ├── conversion.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── conversion.pyi
    │           │   │   │   ├── dtypes.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── dtypes.pyi
    │           │   │   │   ├── fields.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── fields.pyi
    │           │   │   │   ├── nattype.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── nattype.pyi
    │           │   │   │   ├── np_datetime.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── np_datetime.pyi
    │           │   │   │   ├── offsets.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── offsets.pyi
    │           │   │   │   ├── parsing.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── parsing.pyi
    │           │   │   │   ├── period.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── period.pyi
    │           │   │   │   ├── strptime.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── strptime.pyi
    │           │   │   │   ├── timedeltas.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── timedeltas.pyi
    │           │   │   │   ├── timestamps.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── timestamps.pyi
    │           │   │   │   ├── timezones.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── timezones.pyi
    │           │   │   │   ├── tzconversion.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── tzconversion.pyi
    │           │   │   │   ├── vectorized.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   └── vectorized.pyi
    │           │   │   ├── window
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── aggregations.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   ├── aggregations.pyi
    │           │   │   │   ├── indexers.cpython-314-x86_64-linux-gnu.so
    │           │   │   │   └── indexers.pyi
    │           │   │   ├── writers.cpython-314-x86_64-linux-gnu.so
    │           │   │   └── writers.pyi
    │           │   ├── _testing
    │           │   │   ├── __init__.py
    │           │   │   ├── _io.py
    │           │   │   ├── _warnings.py
    │           │   │   ├── asserters.py
    │           │   │   ├── compat.py
    │           │   │   └── contexts.py
    │           │   ├── _typing.py
    │           │   ├── _version_meson.py
    │           │   ├── api
    │           │   │   ├── __init__.py
    │           │   │   ├── executors
    │           │   │   │   └── __init__.py
    │           │   │   ├── extensions
    │           │   │   │   └── __init__.py
    │           │   │   ├── indexers
    │           │   │   │   └── __init__.py
    │           │   │   ├── interchange
    │           │   │   │   └── __init__.py
    │           │   │   ├── internals.py
    │           │   │   ├── types
    │           │   │   │   └── __init__.py
    │           │   │   └── typing
    │           │   │       ├── __init__.py
    │           │   │       └── aliases.py
    │           │   ├── arrays
    │           │   │   └── __init__.py
    │           │   ├── compat
    │           │   │   ├── __init__.py
    │           │   │   ├── _constants.py
    │           │   │   ├── _cpu.py
    │           │   │   ├── _optional.py
    │           │   │   ├── numpy
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── function.py
    │           │   │   ├── pickle_compat.py
    │           │   │   └── pyarrow.py
    │           │   ├── conftest.py
    │           │   ├── core
    │           │   │   ├── __init__.py
    │           │   │   ├── _numba
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── executor.py
    │           │   │   │   ├── extensions.py
    │           │   │   │   └── kernels
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── mean_.py
    │           │   │   │       ├── min_max_.py
    │           │   │   │       ├── shared.py
    │           │   │   │       ├── sum_.py
    │           │   │   │       └── var_.py
    │           │   │   ├── accessor.py
    │           │   │   ├── algorithms.py
    │           │   │   ├── api.py
    │           │   │   ├── apply.py
    │           │   │   ├── array_algos
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── datetimelike_accumulations.py
    │           │   │   │   ├── masked_accumulations.py
    │           │   │   │   ├── masked_reductions.py
    │           │   │   │   ├── putmask.py
    │           │   │   │   ├── quantile.py
    │           │   │   │   ├── replace.py
    │           │   │   │   ├── take.py
    │           │   │   │   └── transforms.py
    │           │   │   ├── arraylike.py
    │           │   │   ├── arrays
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _arrow_string_mixins.py
    │           │   │   │   ├── _mixins.py
    │           │   │   │   ├── _ranges.py
    │           │   │   │   ├── _utils.py
    │           │   │   │   ├── arrow
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── _arrow_utils.py
    │           │   │   │   │   ├── accessors.py
    │           │   │   │   │   ├── array.py
    │           │   │   │   │   └── extension_types.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── boolean.py
    │           │   │   │   ├── categorical.py
    │           │   │   │   ├── datetimelike.py
    │           │   │   │   ├── datetimes.py
    │           │   │   │   ├── floating.py
    │           │   │   │   ├── integer.py
    │           │   │   │   ├── interval.py
    │           │   │   │   ├── masked.py
    │           │   │   │   ├── numeric.py
    │           │   │   │   ├── numpy_.py
    │           │   │   │   ├── period.py
    │           │   │   │   ├── sparse
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── accessor.py
    │           │   │   │   │   ├── array.py
    │           │   │   │   │   └── scipy_sparse.py
    │           │   │   │   ├── string_.py
    │           │   │   │   ├── string_arrow.py
    │           │   │   │   └── timedeltas.py
    │           │   │   ├── base.py
    │           │   │   ├── col.py
    │           │   │   ├── common.py
    │           │   │   ├── computation
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── align.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── check.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── engines.py
    │           │   │   │   ├── eval.py
    │           │   │   │   ├── expr.py
    │           │   │   │   ├── expressions.py
    │           │   │   │   ├── ops.py
    │           │   │   │   ├── parsing.py
    │           │   │   │   ├── pytables.py
    │           │   │   │   └── scope.py
    │           │   │   ├── config_init.py
    │           │   │   ├── construction.py
    │           │   │   ├── dtypes
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── astype.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── cast.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── concat.py
    │           │   │   │   ├── dtypes.py
    │           │   │   │   ├── generic.py
    │           │   │   │   ├── inference.py
    │           │   │   │   └── missing.py
    │           │   │   ├── flags.py
    │           │   │   ├── frame.py
    │           │   │   ├── generic.py
    │           │   │   ├── groupby
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── categorical.py
    │           │   │   │   ├── generic.py
    │           │   │   │   ├── groupby.py
    │           │   │   │   ├── grouper.py
    │           │   │   │   ├── indexing.py
    │           │   │   │   ├── numba_.py
    │           │   │   │   └── ops.py
    │           │   │   ├── indexers
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── objects.py
    │           │   │   │   └── utils.py
    │           │   │   ├── indexes
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── accessors.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── category.py
    │           │   │   │   ├── datetimelike.py
    │           │   │   │   ├── datetimes.py
    │           │   │   │   ├── extension.py
    │           │   │   │   ├── frozen.py
    │           │   │   │   ├── interval.py
    │           │   │   │   ├── multi.py
    │           │   │   │   ├── period.py
    │           │   │   │   ├── range.py
    │           │   │   │   └── timedeltas.py
    │           │   │   ├── indexing.py
    │           │   │   ├── interchange
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── buffer.py
    │           │   │   │   ├── column.py
    │           │   │   │   ├── dataframe.py
    │           │   │   │   ├── dataframe_protocol.py
    │           │   │   │   ├── from_dataframe.py
    │           │   │   │   └── utils.py
    │           │   │   ├── internals
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── blocks.py
    │           │   │   │   ├── concat.py
    │           │   │   │   ├── construction.py
    │           │   │   │   ├── managers.py
    │           │   │   │   └── ops.py
    │           │   │   ├── methods
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── describe.py
    │           │   │   │   ├── filter.py
    │           │   │   │   ├── select.py
    │           │   │   │   ├── selectn.py
    │           │   │   │   └── to_dict.py
    │           │   │   ├── missing.py
    │           │   │   ├── nanops.py
    │           │   │   ├── ops
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── array_ops.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── dispatch.py
    │           │   │   │   ├── invalid.py
    │           │   │   │   ├── mask_ops.py
    │           │   │   │   └── missing.py
    │           │   │   ├── resample.py
    │           │   │   ├── reshape
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── concat.py
    │           │   │   │   ├── encoding.py
    │           │   │   │   ├── melt.py
    │           │   │   │   ├── merge.py
    │           │   │   │   ├── pivot.py
    │           │   │   │   ├── reshape.py
    │           │   │   │   └── tile.py
    │           │   │   ├── roperator.py
    │           │   │   ├── sample.py
    │           │   │   ├── series.py
    │           │   │   ├── sorting.py
    │           │   │   ├── sparse
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── api.py
    │           │   │   ├── strings
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── accessor.py
    │           │   │   │   └── object_array.py
    │           │   │   ├── tools
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── datetimes.py
    │           │   │   │   ├── numeric.py
    │           │   │   │   ├── timedeltas.py
    │           │   │   │   └── times.py
    │           │   │   ├── util
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── hashing.py
    │           │   │   │   └── numba_.py
    │           │   │   └── window
    │           │   │       ├── __init__.py
    │           │   │       ├── common.py
    │           │   │       ├── ewm.py
    │           │   │       ├── expanding.py
    │           │   │       ├── numba_.py
    │           │   │       ├── online.py
    │           │   │       └── rolling.py
    │           │   ├── errors
    │           │   │   ├── __init__.py
    │           │   │   └── cow.py
    │           │   ├── io
    │           │   │   ├── __init__.py
    │           │   │   ├── _util.py
    │           │   │   ├── api.py
    │           │   │   ├── clipboard
    │           │   │   │   └── __init__.py
    │           │   │   ├── clipboards.py
    │           │   │   ├── common.py
    │           │   │   ├── excel
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _base.py
    │           │   │   │   ├── _calamine.py
    │           │   │   │   ├── _odfreader.py
    │           │   │   │   ├── _odswriter.py
    │           │   │   │   ├── _openpyxl.py
    │           │   │   │   ├── _pyxlsb.py
    │           │   │   │   ├── _util.py
    │           │   │   │   ├── _xlrd.py
    │           │   │   │   └── _xlsxwriter.py
    │           │   │   ├── feather_format.py
    │           │   │   ├── formats
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _color_data.py
    │           │   │   │   ├── console.py
    │           │   │   │   ├── css.py
    │           │   │   │   ├── csvs.py
    │           │   │   │   ├── excel.py
    │           │   │   │   ├── format.py
    │           │   │   │   ├── html.py
    │           │   │   │   ├── info.py
    │           │   │   │   ├── printing.py
    │           │   │   │   ├── string.py
    │           │   │   │   ├── style.py
    │           │   │   │   ├── style_render.py
    │           │   │   │   ├── templates
    │           │   │   │   │   ├── html.tpl
    │           │   │   │   │   ├── html_style.tpl
    │           │   │   │   │   ├── html_table.tpl
    │           │   │   │   │   ├── latex.tpl
    │           │   │   │   │   ├── latex_longtable.tpl
    │           │   │   │   │   ├── latex_table.tpl
    │           │   │   │   │   ├── string.tpl
    │           │   │   │   │   └── typst.tpl
    │           │   │   │   └── xml.py
    │           │   │   ├── html.py
    │           │   │   ├── iceberg.py
    │           │   │   ├── json
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _json.py
    │           │   │   │   ├── _normalize.py
    │           │   │   │   └── _table_schema.py
    │           │   │   ├── orc.py
    │           │   │   ├── parquet.py
    │           │   │   ├── parsers
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── arrow_parser_wrapper.py
    │           │   │   │   ├── base_parser.py
    │           │   │   │   ├── c_parser_wrapper.py
    │           │   │   │   ├── python_parser.py
    │           │   │   │   └── readers.py
    │           │   │   ├── pickle.py
    │           │   │   ├── pytables.py
    │           │   │   ├── sas
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── sas7bdat.py
    │           │   │   │   ├── sas_constants.py
    │           │   │   │   ├── sas_xport.py
    │           │   │   │   └── sasreader.py
    │           │   │   ├── spss.py
    │           │   │   ├── sql.py
    │           │   │   ├── stata.py
    │           │   │   └── xml.py
    │           │   ├── plotting
    │           │   │   ├── __init__.py
    │           │   │   ├── _core.py
    │           │   │   ├── _matplotlib
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── boxplot.py
    │           │   │   │   ├── converter.py
    │           │   │   │   ├── core.py
    │           │   │   │   ├── groupby.py
    │           │   │   │   ├── hist.py
    │           │   │   │   ├── misc.py
    │           │   │   │   ├── style.py
    │           │   │   │   ├── timeseries.py
    │           │   │   │   └── tools.py
    │           │   │   └── _misc.py
    │           │   ├── pyproject.toml
    │           │   ├── testing.py
    │           │   ├── tests
    │           │   │   ├── __init__.py
    │           │   │   ├── api
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   └── test_types.py
    │           │   │   ├── apply
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── test_frame_apply.py
    │           │   │   │   ├── test_frame_apply_relabeling.py
    │           │   │   │   ├── test_frame_transform.py
    │           │   │   │   ├── test_invalid_arg.py
    │           │   │   │   ├── test_numba.py
    │           │   │   │   ├── test_series_apply.py
    │           │   │   │   ├── test_series_apply_relabeling.py
    │           │   │   │   ├── test_series_transform.py
    │           │   │   │   └── test_str.py
    │           │   │   ├── arithmetic
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── test_array_ops.py
    │           │   │   │   ├── test_bool.py
    │           │   │   │   ├── test_categorical.py
    │           │   │   │   ├── test_datetime64.py
    │           │   │   │   ├── test_interval.py
    │           │   │   │   ├── test_numeric.py
    │           │   │   │   ├── test_object.py
    │           │   │   │   ├── test_period.py
    │           │   │   │   ├── test_string.py
    │           │   │   │   └── test_timedelta64.py
    │           │   │   ├── arrays
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── arrow
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── common.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── test_concat.py
    │           │   │   │   │   ├── test_conversion.py
    │           │   │   │   │   ├── test_datetimelike.py
    │           │   │   │   │   ├── test_dtype.py
    │           │   │   │   │   ├── test_function.py
    │           │   │   │   │   ├── test_groupby.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_ops.py
    │           │   │   │   │   ├── test_pickle.py
    │           │   │   │   │   ├── test_reductions.py
    │           │   │   │   │   └── test_string.py
    │           │   │   │   ├── boolean
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_comparison.py
    │           │   │   │   │   ├── test_construction.py
    │           │   │   │   │   ├── test_function.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_logical.py
    │           │   │   │   │   ├── test_ops.py
    │           │   │   │   │   ├── test_reduction.py
    │           │   │   │   │   └── test_repr.py
    │           │   │   │   ├── categorical
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_algos.py
    │           │   │   │   │   ├── test_analytics.py
    │           │   │   │   │   ├── test_api.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_dtypes.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_map.py
    │           │   │   │   │   ├── test_missing.py
    │           │   │   │   │   ├── test_operators.py
    │           │   │   │   │   ├── test_replace.py
    │           │   │   │   │   ├── test_repr.py
    │           │   │   │   │   ├── test_sorting.py
    │           │   │   │   │   ├── test_subclass.py
    │           │   │   │   │   ├── test_take.py
    │           │   │   │   │   └── test_warnings.py
    │           │   │   │   ├── datetimes
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_cumulative.py
    │           │   │   │   │   └── test_reductions.py
    │           │   │   │   ├── floating
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_comparison.py
    │           │   │   │   │   ├── test_concat.py
    │           │   │   │   │   ├── test_construction.py
    │           │   │   │   │   ├── test_contains.py
    │           │   │   │   │   ├── test_function.py
    │           │   │   │   │   ├── test_repr.py
    │           │   │   │   │   └── test_to_numpy.py
    │           │   │   │   ├── integer
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_comparison.py
    │           │   │   │   │   ├── test_concat.py
    │           │   │   │   │   ├── test_construction.py
    │           │   │   │   │   ├── test_dtypes.py
    │           │   │   │   │   ├── test_function.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_reduction.py
    │           │   │   │   │   └── test_repr.py
    │           │   │   │   ├── interval
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_interval.py
    │           │   │   │   │   ├── test_interval_pyarrow.py
    │           │   │   │   │   └── test_overlaps.py
    │           │   │   │   ├── masked
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_arrow_compat.py
    │           │   │   │   │   ├── test_function.py
    │           │   │   │   │   └── test_indexing.py
    │           │   │   │   ├── masked_shared.py
    │           │   │   │   ├── numpy_
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   └── test_numpy.py
    │           │   │   │   ├── period
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_arrow_compat.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   └── test_reductions.py
    │           │   │   │   ├── sparse
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_accessor.py
    │           │   │   │   │   ├── test_arithmetics.py
    │           │   │   │   │   ├── test_array.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_combine_concat.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_dtype.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_libsparse.py
    │           │   │   │   │   ├── test_reductions.py
    │           │   │   │   │   └── test_unary.py
    │           │   │   │   ├── string_
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_concat.py
    │           │   │   │   │   ├── test_string.py
    │           │   │   │   │   └── test_string_arrow.py
    │           │   │   │   ├── test_array.py
    │           │   │   │   ├── test_datetimelike.py
    │           │   │   │   ├── test_datetimes.py
    │           │   │   │   ├── test_ndarray_backed.py
    │           │   │   │   ├── test_period.py
    │           │   │   │   ├── test_timedeltas.py
    │           │   │   │   └── timedeltas
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_constructors.py
    │           │   │   │       ├── test_cumulative.py
    │           │   │   │       └── test_reductions.py
    │           │   │   ├── base
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── test_constructors.py
    │           │   │   │   ├── test_conversion.py
    │           │   │   │   ├── test_fillna.py
    │           │   │   │   ├── test_misc.py
    │           │   │   │   ├── test_transpose.py
    │           │   │   │   ├── test_unique.py
    │           │   │   │   └── test_value_counts.py
    │           │   │   ├── computation
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_compat.py
    │           │   │   │   └── test_eval.py
    │           │   │   ├── config
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_config.py
    │           │   │   │   └── test_localization.py
    │           │   │   ├── construction
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── test_extract_array.py
    │           │   │   ├── copy_view
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── index
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_datetimeindex.py
    │           │   │   │   │   ├── test_index.py
    │           │   │   │   │   ├── test_intervalindex.py
    │           │   │   │   │   ├── test_periodindex.py
    │           │   │   │   │   └── test_timedeltaindex.py
    │           │   │   │   ├── test_array.py
    │           │   │   │   ├── test_astype.py
    │           │   │   │   ├── test_chained_assignment_deprecation.py
    │           │   │   │   ├── test_clip.py
    │           │   │   │   ├── test_constructors.py
    │           │   │   │   ├── test_copy_deprecation.py
    │           │   │   │   ├── test_core_functionalities.py
    │           │   │   │   ├── test_functions.py
    │           │   │   │   ├── test_indexing.py
    │           │   │   │   ├── test_internals.py
    │           │   │   │   ├── test_interp_fillna.py
    │           │   │   │   ├── test_methods.py
    │           │   │   │   ├── test_replace.py
    │           │   │   │   ├── test_setitem.py
    │           │   │   │   ├── test_util.py
    │           │   │   │   └── util.py
    │           │   │   ├── dtypes
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── cast
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_box_unbox.py
    │           │   │   │   │   ├── test_can_hold_element.py
    │           │   │   │   │   ├── test_construct_from_scalar.py
    │           │   │   │   │   ├── test_construct_ndarray.py
    │           │   │   │   │   ├── test_construct_object_arr.py
    │           │   │   │   │   ├── test_dict_compat.py
    │           │   │   │   │   ├── test_downcast.py
    │           │   │   │   │   ├── test_find_common_type.py
    │           │   │   │   │   ├── test_infer_datetimelike.py
    │           │   │   │   │   ├── test_infer_dtype.py
    │           │   │   │   │   └── test_promote.py
    │           │   │   │   ├── test_common.py
    │           │   │   │   ├── test_concat.py
    │           │   │   │   ├── test_dtypes.py
    │           │   │   │   ├── test_generic.py
    │           │   │   │   ├── test_inference.py
    │           │   │   │   └── test_missing.py
    │           │   │   ├── extension
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── array_with_attr
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── array.py
    │           │   │   │   │   └── test_array_with_attr.py
    │           │   │   │   ├── base
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── accumulate.py
    │           │   │   │   │   ├── base.py
    │           │   │   │   │   ├── casting.py
    │           │   │   │   │   ├── constructors.py
    │           │   │   │   │   ├── dim2.py
    │           │   │   │   │   ├── dtype.py
    │           │   │   │   │   ├── getitem.py
    │           │   │   │   │   ├── groupby.py
    │           │   │   │   │   ├── index.py
    │           │   │   │   │   ├── interface.py
    │           │   │   │   │   ├── io.py
    │           │   │   │   │   ├── methods.py
    │           │   │   │   │   ├── missing.py
    │           │   │   │   │   ├── ops.py
    │           │   │   │   │   ├── plotting.py
    │           │   │   │   │   ├── printing.py
    │           │   │   │   │   ├── reduce.py
    │           │   │   │   │   ├── reshaping.py
    │           │   │   │   │   └── setitem.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── date
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── array.py
    │           │   │   │   ├── decimal
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── array.py
    │           │   │   │   │   └── test_decimal.py
    │           │   │   │   ├── json
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── array.py
    │           │   │   │   │   └── test_json.py
    │           │   │   │   ├── list
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── array.py
    │           │   │   │   │   └── test_list.py
    │           │   │   │   ├── test_arrow.py
    │           │   │   │   ├── test_categorical.py
    │           │   │   │   ├── test_common.py
    │           │   │   │   ├── test_datetime.py
    │           │   │   │   ├── test_extension.py
    │           │   │   │   ├── test_interval.py
    │           │   │   │   ├── test_masked.py
    │           │   │   │   ├── test_numpy.py
    │           │   │   │   ├── test_period.py
    │           │   │   │   ├── test_sparse.py
    │           │   │   │   ├── test_string.py
    │           │   │   │   └── uuid
    │           │   │   │       ├── __init__.py
    │           │   │   │       └── test_uuid.py
    │           │   │   ├── frame
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── constructors
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_from_dict.py
    │           │   │   │   │   └── test_from_records.py
    │           │   │   │   ├── indexing
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_coercion.py
    │           │   │   │   │   ├── test_delitem.py
    │           │   │   │   │   ├── test_get.py
    │           │   │   │   │   ├── test_get_value.py
    │           │   │   │   │   ├── test_getitem.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_insert.py
    │           │   │   │   │   ├── test_mask.py
    │           │   │   │   │   ├── test_set_value.py
    │           │   │   │   │   ├── test_setitem.py
    │           │   │   │   │   ├── test_take.py
    │           │   │   │   │   ├── test_where.py
    │           │   │   │   │   └── test_xs.py
    │           │   │   │   ├── methods
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_add_prefix_suffix.py
    │           │   │   │   │   ├── test_align.py
    │           │   │   │   │   ├── test_asfreq.py
    │           │   │   │   │   ├── test_asof.py
    │           │   │   │   │   ├── test_assign.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_at_time.py
    │           │   │   │   │   ├── test_between_time.py
    │           │   │   │   │   ├── test_clip.py
    │           │   │   │   │   ├── test_combine.py
    │           │   │   │   │   ├── test_combine_first.py
    │           │   │   │   │   ├── test_compare.py
    │           │   │   │   │   ├── test_convert_dtypes.py
    │           │   │   │   │   ├── test_copy.py
    │           │   │   │   │   ├── test_count.py
    │           │   │   │   │   ├── test_cov_corr.py
    │           │   │   │   │   ├── test_describe.py
    │           │   │   │   │   ├── test_diff.py
    │           │   │   │   │   ├── test_dot.py
    │           │   │   │   │   ├── test_drop.py
    │           │   │   │   │   ├── test_drop_duplicates.py
    │           │   │   │   │   ├── test_droplevel.py
    │           │   │   │   │   ├── test_dropna.py
    │           │   │   │   │   ├── test_dtypes.py
    │           │   │   │   │   ├── test_duplicated.py
    │           │   │   │   │   ├── test_equals.py
    │           │   │   │   │   ├── test_explode.py
    │           │   │   │   │   ├── test_fillna.py
    │           │   │   │   │   ├── test_filter.py
    │           │   │   │   │   ├── test_first_valid_index.py
    │           │   │   │   │   ├── test_get_numeric_data.py
    │           │   │   │   │   ├── test_head_tail.py
    │           │   │   │   │   ├── test_infer_objects.py
    │           │   │   │   │   ├── test_info.py
    │           │   │   │   │   ├── test_interpolate.py
    │           │   │   │   │   ├── test_is_homogeneous_dtype.py
    │           │   │   │   │   ├── test_isetitem.py
    │           │   │   │   │   ├── test_isin.py
    │           │   │   │   │   ├── test_iterrows.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_map.py
    │           │   │   │   │   ├── test_matmul.py
    │           │   │   │   │   ├── test_nlargest.py
    │           │   │   │   │   ├── test_pct_change.py
    │           │   │   │   │   ├── test_pipe.py
    │           │   │   │   │   ├── test_pop.py
    │           │   │   │   │   ├── test_quantile.py
    │           │   │   │   │   ├── test_rank.py
    │           │   │   │   │   ├── test_reindex.py
    │           │   │   │   │   ├── test_reindex_like.py
    │           │   │   │   │   ├── test_rename.py
    │           │   │   │   │   ├── test_rename_axis.py
    │           │   │   │   │   ├── test_reorder_levels.py
    │           │   │   │   │   ├── test_replace.py
    │           │   │   │   │   ├── test_reset_index.py
    │           │   │   │   │   ├── test_round.py
    │           │   │   │   │   ├── test_sample.py
    │           │   │   │   │   ├── test_select.py
    │           │   │   │   │   ├── test_select_dtypes.py
    │           │   │   │   │   ├── test_set_axis.py
    │           │   │   │   │   ├── test_set_index.py
    │           │   │   │   │   ├── test_shift.py
    │           │   │   │   │   ├── test_size.py
    │           │   │   │   │   ├── test_sort_index.py
    │           │   │   │   │   ├── test_sort_values.py
    │           │   │   │   │   ├── test_swaplevel.py
    │           │   │   │   │   ├── test_to_csv.py
    │           │   │   │   │   ├── test_to_dict.py
    │           │   │   │   │   ├── test_to_dict_of_blocks.py
    │           │   │   │   │   ├── test_to_numpy.py
    │           │   │   │   │   ├── test_to_period.py
    │           │   │   │   │   ├── test_to_records.py
    │           │   │   │   │   ├── test_to_timestamp.py
    │           │   │   │   │   ├── test_transpose.py
    │           │   │   │   │   ├── test_truncate.py
    │           │   │   │   │   ├── test_tz_convert.py
    │           │   │   │   │   ├── test_tz_localize.py
    │           │   │   │   │   ├── test_update.py
    │           │   │   │   │   ├── test_value_counts.py
    │           │   │   │   │   └── test_values.py
    │           │   │   │   ├── test_alter_axes.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   ├── test_arithmetic.py
    │           │   │   │   ├── test_arrow_interface.py
    │           │   │   │   ├── test_block_internals.py
    │           │   │   │   ├── test_constructors.py
    │           │   │   │   ├── test_cumulative.py
    │           │   │   │   ├── test_iteration.py
    │           │   │   │   ├── test_logical_ops.py
    │           │   │   │   ├── test_nonunique_indexes.py
    │           │   │   │   ├── test_npfuncs.py
    │           │   │   │   ├── test_query_eval.py
    │           │   │   │   ├── test_reductions.py
    │           │   │   │   ├── test_repr.py
    │           │   │   │   ├── test_stack_unstack.py
    │           │   │   │   ├── test_subclass.py
    │           │   │   │   ├── test_ufunc.py
    │           │   │   │   ├── test_unary.py
    │           │   │   │   └── test_validate.py
    │           │   │   ├── generic
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_duplicate_labels.py
    │           │   │   │   ├── test_finalize.py
    │           │   │   │   ├── test_frame.py
    │           │   │   │   ├── test_generic.py
    │           │   │   │   ├── test_label_or_level_utils.py
    │           │   │   │   ├── test_series.py
    │           │   │   │   └── test_to_xarray.py
    │           │   │   ├── groupby
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── aggregate
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_aggregate.py
    │           │   │   │   │   ├── test_cython.py
    │           │   │   │   │   ├── test_numba.py
    │           │   │   │   │   └── test_other.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── methods
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_describe.py
    │           │   │   │   │   ├── test_groupby_shift_diff.py
    │           │   │   │   │   ├── test_is_monotonic.py
    │           │   │   │   │   ├── test_kurt.py
    │           │   │   │   │   ├── test_nlargest_nsmallest.py
    │           │   │   │   │   ├── test_nth.py
    │           │   │   │   │   ├── test_quantile.py
    │           │   │   │   │   ├── test_rank.py
    │           │   │   │   │   ├── test_sample.py
    │           │   │   │   │   ├── test_size.py
    │           │   │   │   │   ├── test_skew.py
    │           │   │   │   │   └── test_value_counts.py
    │           │   │   │   ├── test_all_methods.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   ├── test_apply.py
    │           │   │   │   ├── test_bin_groupby.py
    │           │   │   │   ├── test_categorical.py
    │           │   │   │   ├── test_counting.py
    │           │   │   │   ├── test_cumulative.py
    │           │   │   │   ├── test_filters.py
    │           │   │   │   ├── test_groupby.py
    │           │   │   │   ├── test_groupby_dropna.py
    │           │   │   │   ├── test_groupby_subclass.py
    │           │   │   │   ├── test_grouping.py
    │           │   │   │   ├── test_index_as_string.py
    │           │   │   │   ├── test_indexing.py
    │           │   │   │   ├── test_libgroupby.py
    │           │   │   │   ├── test_missing.py
    │           │   │   │   ├── test_numba.py
    │           │   │   │   ├── test_numeric_only.py
    │           │   │   │   ├── test_pipe.py
    │           │   │   │   ├── test_raises.py
    │           │   │   │   ├── test_reductions.py
    │           │   │   │   ├── test_sparse.py
    │           │   │   │   ├── test_timegrouper.py
    │           │   │   │   └── transform
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── test_numba.py
    │           │   │   │       └── test_transform.py
    │           │   │   ├── indexes
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base_class
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_pickle.py
    │           │   │   │   │   ├── test_reshape.py
    │           │   │   │   │   ├── test_setops.py
    │           │   │   │   │   └── test_where.py
    │           │   │   │   ├── categorical
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_append.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_category.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_equals.py
    │           │   │   │   │   ├── test_fillna.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_map.py
    │           │   │   │   │   ├── test_reindex.py
    │           │   │   │   │   └── test_setops.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── datetimelike_
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_drop_duplicates.py
    │           │   │   │   │   ├── test_equals.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_is_monotonic.py
    │           │   │   │   │   ├── test_nat.py
    │           │   │   │   │   ├── test_sort_values.py
    │           │   │   │   │   └── test_value_counts.py
    │           │   │   │   ├── datetimes
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── methods
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── test_asof.py
    │           │   │   │   │   │   ├── test_astype.py
    │           │   │   │   │   │   ├── test_delete.py
    │           │   │   │   │   │   ├── test_factorize.py
    │           │   │   │   │   │   ├── test_fillna.py
    │           │   │   │   │   │   ├── test_insert.py
    │           │   │   │   │   │   ├── test_isocalendar.py
    │           │   │   │   │   │   ├── test_map.py
    │           │   │   │   │   │   ├── test_normalize.py
    │           │   │   │   │   │   ├── test_repeat.py
    │           │   │   │   │   │   ├── test_resolution.py
    │           │   │   │   │   │   ├── test_round.py
    │           │   │   │   │   │   ├── test_shift.py
    │           │   │   │   │   │   ├── test_snap.py
    │           │   │   │   │   │   ├── test_to_frame.py
    │           │   │   │   │   │   ├── test_to_julian_date.py
    │           │   │   │   │   │   ├── test_to_period.py
    │           │   │   │   │   │   ├── test_to_pydatetime.py
    │           │   │   │   │   │   ├── test_to_series.py
    │           │   │   │   │   │   ├── test_tz_convert.py
    │           │   │   │   │   │   ├── test_tz_localize.py
    │           │   │   │   │   │   └── test_unique.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_date_range.py
    │           │   │   │   │   ├── test_datetime.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_freq_attr.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_iter.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_npfuncs.py
    │           │   │   │   │   ├── test_ops.py
    │           │   │   │   │   ├── test_partial_slicing.py
    │           │   │   │   │   ├── test_pickle.py
    │           │   │   │   │   ├── test_reindex.py
    │           │   │   │   │   ├── test_scalar_compat.py
    │           │   │   │   │   ├── test_setops.py
    │           │   │   │   │   └── test_timezones.py
    │           │   │   │   ├── interval
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_equals.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_interval.py
    │           │   │   │   │   ├── test_interval_range.py
    │           │   │   │   │   ├── test_interval_tree.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_pickle.py
    │           │   │   │   │   └── test_setops.py
    │           │   │   │   ├── multi
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── test_analytics.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_compat.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_conversion.py
    │           │   │   │   │   ├── test_copy.py
    │           │   │   │   │   ├── test_drop.py
    │           │   │   │   │   ├── test_duplicates.py
    │           │   │   │   │   ├── test_equivalence.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_get_level_values.py
    │           │   │   │   │   ├── test_get_set.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_integrity.py
    │           │   │   │   │   ├── test_isin.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_lexsort.py
    │           │   │   │   │   ├── test_missing.py
    │           │   │   │   │   ├── test_monotonic.py
    │           │   │   │   │   ├── test_names.py
    │           │   │   │   │   ├── test_partial_indexing.py
    │           │   │   │   │   ├── test_pickle.py
    │           │   │   │   │   ├── test_reindex.py
    │           │   │   │   │   ├── test_reshape.py
    │           │   │   │   │   ├── test_setops.py
    │           │   │   │   │   ├── test_sorting.py
    │           │   │   │   │   ├── test_take.py
    │           │   │   │   │   └── test_util.py
    │           │   │   │   ├── numeric
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_numeric.py
    │           │   │   │   │   └── test_setops.py
    │           │   │   │   ├── object
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   └── test_indexing.py
    │           │   │   │   ├── period
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── methods
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── test_asfreq.py
    │           │   │   │   │   │   ├── test_astype.py
    │           │   │   │   │   │   ├── test_factorize.py
    │           │   │   │   │   │   ├── test_fillna.py
    │           │   │   │   │   │   ├── test_insert.py
    │           │   │   │   │   │   ├── test_is_full.py
    │           │   │   │   │   │   ├── test_repeat.py
    │           │   │   │   │   │   ├── test_shift.py
    │           │   │   │   │   │   └── test_to_timestamp.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_freq_attr.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_monotonic.py
    │           │   │   │   │   ├── test_partial_slicing.py
    │           │   │   │   │   ├── test_period.py
    │           │   │   │   │   ├── test_period_range.py
    │           │   │   │   │   ├── test_pickle.py
    │           │   │   │   │   ├── test_resolution.py
    │           │   │   │   │   ├── test_scalar_compat.py
    │           │   │   │   │   ├── test_searchsorted.py
    │           │   │   │   │   ├── test_setops.py
    │           │   │   │   │   └── test_tools.py
    │           │   │   │   ├── ranges
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_range.py
    │           │   │   │   │   └── test_setops.py
    │           │   │   │   ├── string
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   └── test_indexing.py
    │           │   │   │   ├── test_any_index.py
    │           │   │   │   ├── test_base.py
    │           │   │   │   ├── test_common.py
    │           │   │   │   ├── test_datetimelike.py
    │           │   │   │   ├── test_engines.py
    │           │   │   │   ├── test_frozen.py
    │           │   │   │   ├── test_index_new.py
    │           │   │   │   ├── test_indexing.py
    │           │   │   │   ├── test_numpy_compat.py
    │           │   │   │   ├── test_old_base.py
    │           │   │   │   ├── test_setops.py
    │           │   │   │   ├── test_subclass.py
    │           │   │   │   └── timedeltas
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── methods
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── test_astype.py
    │           │   │   │       │   ├── test_factorize.py
    │           │   │   │       │   ├── test_fillna.py
    │           │   │   │       │   ├── test_insert.py
    │           │   │   │       │   ├── test_repeat.py
    │           │   │   │       │   ├── test_resolution.py
    │           │   │   │       │   └── test_shift.py
    │           │   │   │       ├── test_arithmetic.py
    │           │   │   │       ├── test_constructors.py
    │           │   │   │       ├── test_delete.py
    │           │   │   │       ├── test_formats.py
    │           │   │   │       ├── test_freq_attr.py
    │           │   │   │       ├── test_indexing.py
    │           │   │   │       ├── test_join.py
    │           │   │   │       ├── test_ops.py
    │           │   │   │       ├── test_pickle.py
    │           │   │   │       ├── test_scalar_compat.py
    │           │   │   │       ├── test_searchsorted.py
    │           │   │   │       ├── test_setops.py
    │           │   │   │       ├── test_timedelta.py
    │           │   │   │       └── test_timedelta_range.py
    │           │   │   ├── indexing
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── interval
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_interval.py
    │           │   │   │   │   └── test_interval_new.py
    │           │   │   │   ├── multiindex
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_chaining_and_caching.py
    │           │   │   │   │   ├── test_datetime.py
    │           │   │   │   │   ├── test_getitem.py
    │           │   │   │   │   ├── test_iloc.py
    │           │   │   │   │   ├── test_indexing_slow.py
    │           │   │   │   │   ├── test_loc.py
    │           │   │   │   │   ├── test_multiindex.py
    │           │   │   │   │   ├── test_partial.py
    │           │   │   │   │   ├── test_setitem.py
    │           │   │   │   │   ├── test_slice.py
    │           │   │   │   │   └── test_sorted.py
    │           │   │   │   ├── test_at.py
    │           │   │   │   ├── test_categorical.py
    │           │   │   │   ├── test_chaining_and_caching.py
    │           │   │   │   ├── test_check_indexer.py
    │           │   │   │   ├── test_coercion.py
    │           │   │   │   ├── test_datetime.py
    │           │   │   │   ├── test_floats.py
    │           │   │   │   ├── test_iat.py
    │           │   │   │   ├── test_iloc.py
    │           │   │   │   ├── test_indexers.py
    │           │   │   │   ├── test_indexing.py
    │           │   │   │   ├── test_loc.py
    │           │   │   │   ├── test_na_indexing.py
    │           │   │   │   ├── test_partial.py
    │           │   │   │   └── test_scalar.py
    │           │   │   ├── interchange
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_impl.py
    │           │   │   │   ├── test_spec_conformance.py
    │           │   │   │   └── test_utils.py
    │           │   │   ├── internals
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   └── test_internals.py
    │           │   │   ├── io
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── excel
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_odf.py
    │           │   │   │   │   ├── test_odswriter.py
    │           │   │   │   │   ├── test_openpyxl.py
    │           │   │   │   │   ├── test_readers.py
    │           │   │   │   │   ├── test_style.py
    │           │   │   │   │   ├── test_writers.py
    │           │   │   │   │   ├── test_xlrd.py
    │           │   │   │   │   └── test_xlsxwriter.py
    │           │   │   │   ├── formats
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── style
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── test_bar.py
    │           │   │   │   │   │   ├── test_exceptions.py
    │           │   │   │   │   │   ├── test_format.py
    │           │   │   │   │   │   ├── test_highlight.py
    │           │   │   │   │   │   ├── test_html.py
    │           │   │   │   │   │   ├── test_matplotlib.py
    │           │   │   │   │   │   ├── test_non_unique.py
    │           │   │   │   │   │   ├── test_style.py
    │           │   │   │   │   │   ├── test_to_latex.py
    │           │   │   │   │   │   ├── test_to_string.py
    │           │   │   │   │   │   ├── test_to_typst.py
    │           │   │   │   │   │   └── test_tooltip.py
    │           │   │   │   │   ├── test_console.py
    │           │   │   │   │   ├── test_css.py
    │           │   │   │   │   ├── test_eng_formatting.py
    │           │   │   │   │   ├── test_format.py
    │           │   │   │   │   ├── test_ipython_compat.py
    │           │   │   │   │   ├── test_printing.py
    │           │   │   │   │   ├── test_to_csv.py
    │           │   │   │   │   ├── test_to_excel.py
    │           │   │   │   │   ├── test_to_html.py
    │           │   │   │   │   ├── test_to_latex.py
    │           │   │   │   │   ├── test_to_markdown.py
    │           │   │   │   │   └── test_to_string.py
    │           │   │   │   ├── generate_legacy_storage_files.py
    │           │   │   │   ├── json
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── test_compression.py
    │           │   │   │   │   ├── test_deprecated_kwargs.py
    │           │   │   │   │   ├── test_json_table_schema.py
    │           │   │   │   │   ├── test_json_table_schema_ext_dtype.py
    │           │   │   │   │   ├── test_normalize.py
    │           │   │   │   │   ├── test_pandas.py
    │           │   │   │   │   ├── test_readlines.py
    │           │   │   │   │   └── test_ujson.py
    │           │   │   │   ├── parser
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── common
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── test_chunksize.py
    │           │   │   │   │   │   ├── test_common_basic.py
    │           │   │   │   │   │   ├── test_data_list.py
    │           │   │   │   │   │   ├── test_decimal.py
    │           │   │   │   │   │   ├── test_file_buffer_url.py
    │           │   │   │   │   │   ├── test_float.py
    │           │   │   │   │   │   ├── test_index.py
    │           │   │   │   │   │   ├── test_inf.py
    │           │   │   │   │   │   ├── test_ints.py
    │           │   │   │   │   │   ├── test_iterator.py
    │           │   │   │   │   │   └── test_read_errors.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── dtypes
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── test_categorical.py
    │           │   │   │   │   │   ├── test_dtypes_basic.py
    │           │   │   │   │   │   └── test_empty.py
    │           │   │   │   │   ├── test_c_parser_only.py
    │           │   │   │   │   ├── test_comment.py
    │           │   │   │   │   ├── test_compression.py
    │           │   │   │   │   ├── test_concatenate_chunks.py
    │           │   │   │   │   ├── test_converters.py
    │           │   │   │   │   ├── test_dialect.py
    │           │   │   │   │   ├── test_encoding.py
    │           │   │   │   │   ├── test_header.py
    │           │   │   │   │   ├── test_index_col.py
    │           │   │   │   │   ├── test_mangle_dupes.py
    │           │   │   │   │   ├── test_multi_thread.py
    │           │   │   │   │   ├── test_na_values.py
    │           │   │   │   │   ├── test_network.py
    │           │   │   │   │   ├── test_parallel_read.py
    │           │   │   │   │   ├── test_parse_dates.py
    │           │   │   │   │   ├── test_python_parser_only.py
    │           │   │   │   │   ├── test_quoting.py
    │           │   │   │   │   ├── test_read_fwf.py
    │           │   │   │   │   ├── test_skiprows.py
    │           │   │   │   │   ├── test_textreader.py
    │           │   │   │   │   ├── test_unsupported.py
    │           │   │   │   │   ├── test_upcast.py
    │           │   │   │   │   └── usecols
    │           │   │   │   │       ├── __init__.py
    │           │   │   │   │       ├── test_parse_dates.py
    │           │   │   │   │       ├── test_strings.py
    │           │   │   │   │       └── test_usecols_basic.py
    │           │   │   │   ├── pytables
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── common.py
    │           │   │   │   │   ├── conftest.py
    │           │   │   │   │   ├── test_append.py
    │           │   │   │   │   ├── test_categorical.py
    │           │   │   │   │   ├── test_compat.py
    │           │   │   │   │   ├── test_complex.py
    │           │   │   │   │   ├── test_errors.py
    │           │   │   │   │   ├── test_file_handling.py
    │           │   │   │   │   ├── test_keys.py
    │           │   │   │   │   ├── test_put.py
    │           │   │   │   │   ├── test_pytables_missing.py
    │           │   │   │   │   ├── test_read.py
    │           │   │   │   │   ├── test_retain_attributes.py
    │           │   │   │   │   ├── test_round_trip.py
    │           │   │   │   │   ├── test_select.py
    │           │   │   │   │   ├── test_store.py
    │           │   │   │   │   ├── test_subclass.py
    │           │   │   │   │   ├── test_time_series.py
    │           │   │   │   │   └── test_timezones.py
    │           │   │   │   ├── sas
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_byteswap.py
    │           │   │   │   │   ├── test_sas.py
    │           │   │   │   │   ├── test_sas7bdat.py
    │           │   │   │   │   └── test_xport.py
    │           │   │   │   ├── test_clipboard.py
    │           │   │   │   ├── test_common.py
    │           │   │   │   ├── test_compression.py
    │           │   │   │   ├── test_feather.py
    │           │   │   │   ├── test_fsspec.py
    │           │   │   │   ├── test_gcs.py
    │           │   │   │   ├── test_html.py
    │           │   │   │   ├── test_http_headers.py
    │           │   │   │   ├── test_iceberg.py
    │           │   │   │   ├── test_orc.py
    │           │   │   │   ├── test_parquet.py
    │           │   │   │   ├── test_pickle.py
    │           │   │   │   ├── test_s3.py
    │           │   │   │   ├── test_spss.py
    │           │   │   │   ├── test_sql.py
    │           │   │   │   ├── test_stata.py
    │           │   │   │   ├── test_util.py
    │           │   │   │   └── xml
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── conftest.py
    │           │   │   │       ├── test_to_xml.py
    │           │   │   │       ├── test_xml.py
    │           │   │   │       └── test_xml_dtypes.py
    │           │   │   ├── libs
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_hashtable.py
    │           │   │   │   ├── test_join.py
    │           │   │   │   ├── test_lib.py
    │           │   │   │   └── test_libalgos.py
    │           │   │   ├── plotting
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── frame
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_frame.py
    │           │   │   │   │   ├── test_frame_color.py
    │           │   │   │   │   ├── test_frame_groupby.py
    │           │   │   │   │   ├── test_frame_legend.py
    │           │   │   │   │   ├── test_frame_subplots.py
    │           │   │   │   │   └── test_hist_box_by.py
    │           │   │   │   ├── test_backend.py
    │           │   │   │   ├── test_boxplot_method.py
    │           │   │   │   ├── test_common.py
    │           │   │   │   ├── test_converter.py
    │           │   │   │   ├── test_datetimelike.py
    │           │   │   │   ├── test_groupby.py
    │           │   │   │   ├── test_hist_method.py
    │           │   │   │   ├── test_misc.py
    │           │   │   │   ├── test_series.py
    │           │   │   │   └── test_style.py
    │           │   │   ├── reductions
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_reductions.py
    │           │   │   │   └── test_stat_reductions.py
    │           │   │   ├── resample
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── test_base.py
    │           │   │   │   ├── test_datetime_index.py
    │           │   │   │   ├── test_period_index.py
    │           │   │   │   ├── test_resample_api.py
    │           │   │   │   ├── test_resampler_grouper.py
    │           │   │   │   ├── test_time_grouper.py
    │           │   │   │   └── test_timedelta.py
    │           │   │   ├── reshape
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── concat
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_append.py
    │           │   │   │   │   ├── test_append_common.py
    │           │   │   │   │   ├── test_categorical.py
    │           │   │   │   │   ├── test_concat.py
    │           │   │   │   │   ├── test_dataframe.py
    │           │   │   │   │   ├── test_datetimes.py
    │           │   │   │   │   ├── test_empty.py
    │           │   │   │   │   ├── test_index.py
    │           │   │   │   │   ├── test_invalid.py
    │           │   │   │   │   ├── test_series.py
    │           │   │   │   │   └── test_sort.py
    │           │   │   │   ├── merge
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_join.py
    │           │   │   │   │   ├── test_merge.py
    │           │   │   │   │   ├── test_merge_antijoin.py
    │           │   │   │   │   ├── test_merge_asof.py
    │           │   │   │   │   ├── test_merge_cross.py
    │           │   │   │   │   ├── test_merge_index_as_string.py
    │           │   │   │   │   ├── test_merge_ordered.py
    │           │   │   │   │   └── test_multi.py
    │           │   │   │   ├── test_crosstab.py
    │           │   │   │   ├── test_cut.py
    │           │   │   │   ├── test_from_dummies.py
    │           │   │   │   ├── test_get_dummies.py
    │           │   │   │   ├── test_melt.py
    │           │   │   │   ├── test_pivot.py
    │           │   │   │   ├── test_pivot_multilevel.py
    │           │   │   │   ├── test_qcut.py
    │           │   │   │   └── test_union_categoricals.py
    │           │   │   ├── scalar
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── interval
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_contains.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   ├── test_interval.py
    │           │   │   │   │   └── test_overlaps.py
    │           │   │   │   ├── period
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_asfreq.py
    │           │   │   │   │   └── test_period.py
    │           │   │   │   ├── test_na_scalar.py
    │           │   │   │   ├── test_nat.py
    │           │   │   │   ├── timedelta
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── methods
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── test_as_unit.py
    │           │   │   │   │   │   └── test_round.py
    │           │   │   │   │   ├── test_arithmetic.py
    │           │   │   │   │   ├── test_constructors.py
    │           │   │   │   │   ├── test_formats.py
    │           │   │   │   │   └── test_timedelta.py
    │           │   │   │   └── timestamp
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── methods
    │           │   │   │       │   ├── __init__.py
    │           │   │   │       │   ├── test_as_unit.py
    │           │   │   │       │   ├── test_normalize.py
    │           │   │   │       │   ├── test_replace.py
    │           │   │   │       │   ├── test_round.py
    │           │   │   │       │   ├── test_timestamp_method.py
    │           │   │   │       │   ├── test_to_julian_date.py
    │           │   │   │       │   ├── test_to_pydatetime.py
    │           │   │   │       │   ├── test_tz_convert.py
    │           │   │   │       │   └── test_tz_localize.py
    │           │   │   │       ├── test_arithmetic.py
    │           │   │   │       ├── test_comparisons.py
    │           │   │   │       ├── test_constructors.py
    │           │   │   │       ├── test_formats.py
    │           │   │   │       ├── test_timestamp.py
    │           │   │   │       └── test_timezones.py
    │           │   │   ├── series
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── accessors
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_cat_accessor.py
    │           │   │   │   │   ├── test_dt_accessor.py
    │           │   │   │   │   ├── test_list_accessor.py
    │           │   │   │   │   ├── test_sparse_accessor.py
    │           │   │   │   │   ├── test_str_accessor.py
    │           │   │   │   │   └── test_struct_accessor.py
    │           │   │   │   ├── indexing
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_datetime.py
    │           │   │   │   │   ├── test_delitem.py
    │           │   │   │   │   ├── test_get.py
    │           │   │   │   │   ├── test_getitem.py
    │           │   │   │   │   ├── test_indexing.py
    │           │   │   │   │   ├── test_mask.py
    │           │   │   │   │   ├── test_set_value.py
    │           │   │   │   │   ├── test_setitem.py
    │           │   │   │   │   ├── test_take.py
    │           │   │   │   │   ├── test_where.py
    │           │   │   │   │   └── test_xs.py
    │           │   │   │   ├── methods
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_add_prefix_suffix.py
    │           │   │   │   │   ├── test_align.py
    │           │   │   │   │   ├── test_argsort.py
    │           │   │   │   │   ├── test_asof.py
    │           │   │   │   │   ├── test_astype.py
    │           │   │   │   │   ├── test_autocorr.py
    │           │   │   │   │   ├── test_between.py
    │           │   │   │   │   ├── test_case_when.py
    │           │   │   │   │   ├── test_clip.py
    │           │   │   │   │   ├── test_combine.py
    │           │   │   │   │   ├── test_combine_first.py
    │           │   │   │   │   ├── test_compare.py
    │           │   │   │   │   ├── test_convert_dtypes.py
    │           │   │   │   │   ├── test_copy.py
    │           │   │   │   │   ├── test_count.py
    │           │   │   │   │   ├── test_cov_corr.py
    │           │   │   │   │   ├── test_describe.py
    │           │   │   │   │   ├── test_diff.py
    │           │   │   │   │   ├── test_drop.py
    │           │   │   │   │   ├── test_drop_duplicates.py
    │           │   │   │   │   ├── test_dropna.py
    │           │   │   │   │   ├── test_dtypes.py
    │           │   │   │   │   ├── test_duplicated.py
    │           │   │   │   │   ├── test_equals.py
    │           │   │   │   │   ├── test_explode.py
    │           │   │   │   │   ├── test_fillna.py
    │           │   │   │   │   ├── test_filter.py
    │           │   │   │   │   ├── test_get_numeric_data.py
    │           │   │   │   │   ├── test_head_tail.py
    │           │   │   │   │   ├── test_infer_objects.py
    │           │   │   │   │   ├── test_info.py
    │           │   │   │   │   ├── test_interpolate.py
    │           │   │   │   │   ├── test_is_monotonic.py
    │           │   │   │   │   ├── test_is_unique.py
    │           │   │   │   │   ├── test_isin.py
    │           │   │   │   │   ├── test_isna.py
    │           │   │   │   │   ├── test_item.py
    │           │   │   │   │   ├── test_map.py
    │           │   │   │   │   ├── test_matmul.py
    │           │   │   │   │   ├── test_nlargest.py
    │           │   │   │   │   ├── test_nunique.py
    │           │   │   │   │   ├── test_pct_change.py
    │           │   │   │   │   ├── test_pop.py
    │           │   │   │   │   ├── test_quantile.py
    │           │   │   │   │   ├── test_rank.py
    │           │   │   │   │   ├── test_reindex.py
    │           │   │   │   │   ├── test_reindex_like.py
    │           │   │   │   │   ├── test_rename.py
    │           │   │   │   │   ├── test_rename_axis.py
    │           │   │   │   │   ├── test_repeat.py
    │           │   │   │   │   ├── test_replace.py
    │           │   │   │   │   ├── test_reset_index.py
    │           │   │   │   │   ├── test_round.py
    │           │   │   │   │   ├── test_searchsorted.py
    │           │   │   │   │   ├── test_set_name.py
    │           │   │   │   │   ├── test_size.py
    │           │   │   │   │   ├── test_sort_index.py
    │           │   │   │   │   ├── test_sort_values.py
    │           │   │   │   │   ├── test_to_csv.py
    │           │   │   │   │   ├── test_to_dict.py
    │           │   │   │   │   ├── test_to_frame.py
    │           │   │   │   │   ├── test_to_numpy.py
    │           │   │   │   │   ├── test_tolist.py
    │           │   │   │   │   ├── test_truncate.py
    │           │   │   │   │   ├── test_tz_localize.py
    │           │   │   │   │   ├── test_unique.py
    │           │   │   │   │   ├── test_unstack.py
    │           │   │   │   │   ├── test_update.py
    │           │   │   │   │   ├── test_value_counts.py
    │           │   │   │   │   └── test_values.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   ├── test_arithmetic.py
    │           │   │   │   ├── test_arrow_interface.py
    │           │   │   │   ├── test_constructors.py
    │           │   │   │   ├── test_cumulative.py
    │           │   │   │   ├── test_formats.py
    │           │   │   │   ├── test_iteration.py
    │           │   │   │   ├── test_logical_ops.py
    │           │   │   │   ├── test_missing.py
    │           │   │   │   ├── test_npfuncs.py
    │           │   │   │   ├── test_reductions.py
    │           │   │   │   ├── test_subclass.py
    │           │   │   │   ├── test_ufunc.py
    │           │   │   │   ├── test_unary.py
    │           │   │   │   └── test_validate.py
    │           │   │   ├── strings
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   ├── test_case_justify.py
    │           │   │   │   ├── test_cat.py
    │           │   │   │   ├── test_extract.py
    │           │   │   │   ├── test_find_replace.py
    │           │   │   │   ├── test_get_dummies.py
    │           │   │   │   ├── test_split_partition.py
    │           │   │   │   ├── test_string_array.py
    │           │   │   │   └── test_strings.py
    │           │   │   ├── test_aggregation.py
    │           │   │   ├── test_algos.py
    │           │   │   ├── test_col.py
    │           │   │   ├── test_common.py
    │           │   │   ├── test_cpu.py
    │           │   │   ├── test_downstream.py
    │           │   │   ├── test_errors.py
    │           │   │   ├── test_expressions.py
    │           │   │   ├── test_flags.py
    │           │   │   ├── test_multilevel.py
    │           │   │   ├── test_nanops.py
    │           │   │   ├── test_optional_dependency.py
    │           │   │   ├── test_register_accessor.py
    │           │   │   ├── test_sorting.py
    │           │   │   ├── test_take.py
    │           │   │   ├── tools
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_to_datetime.py
    │           │   │   │   ├── test_to_numeric.py
    │           │   │   │   ├── test_to_time.py
    │           │   │   │   └── test_to_timedelta.py
    │           │   │   ├── tseries
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── frequencies
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_freq_code.py
    │           │   │   │   │   ├── test_frequencies.py
    │           │   │   │   │   └── test_inference.py
    │           │   │   │   ├── holiday
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── test_calendar.py
    │           │   │   │   │   ├── test_federal.py
    │           │   │   │   │   ├── test_holiday.py
    │           │   │   │   │   └── test_observance.py
    │           │   │   │   └── offsets
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── common.py
    │           │   │   │       ├── test_business_day.py
    │           │   │   │       ├── test_business_halfyear.py
    │           │   │   │       ├── test_business_hour.py
    │           │   │   │       ├── test_business_month.py
    │           │   │   │       ├── test_business_quarter.py
    │           │   │   │       ├── test_business_year.py
    │           │   │   │       ├── test_common.py
    │           │   │   │       ├── test_custom_business_day.py
    │           │   │   │       ├── test_custom_business_hour.py
    │           │   │   │       ├── test_custom_business_month.py
    │           │   │   │       ├── test_dst.py
    │           │   │   │       ├── test_easter.py
    │           │   │   │       ├── test_fiscal.py
    │           │   │   │       ├── test_halfyear.py
    │           │   │   │       ├── test_index.py
    │           │   │   │       ├── test_month.py
    │           │   │   │       ├── test_offsets.py
    │           │   │   │       ├── test_offsets_properties.py
    │           │   │   │       ├── test_quarter.py
    │           │   │   │       ├── test_ticks.py
    │           │   │   │       ├── test_week.py
    │           │   │   │       └── test_year.py
    │           │   │   ├── tslibs
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_api.py
    │           │   │   │   ├── test_array_to_datetime.py
    │           │   │   │   ├── test_ccalendar.py
    │           │   │   │   ├── test_conversion.py
    │           │   │   │   ├── test_fields.py
    │           │   │   │   ├── test_libfrequencies.py
    │           │   │   │   ├── test_liboffsets.py
    │           │   │   │   ├── test_np_datetime.py
    │           │   │   │   ├── test_npy_units.py
    │           │   │   │   ├── test_parse_iso8601.py
    │           │   │   │   ├── test_parsing.py
    │           │   │   │   ├── test_period.py
    │           │   │   │   ├── test_resolution.py
    │           │   │   │   ├── test_strptime.py
    │           │   │   │   ├── test_timedeltas.py
    │           │   │   │   ├── test_timezones.py
    │           │   │   │   ├── test_to_offset.py
    │           │   │   │   └── test_tzconversion.py
    │           │   │   ├── util
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── conftest.py
    │           │   │   │   ├── test_assert_almost_equal.py
    │           │   │   │   ├── test_assert_attr_equal.py
    │           │   │   │   ├── test_assert_categorical_equal.py
    │           │   │   │   ├── test_assert_extension_array_equal.py
    │           │   │   │   ├── test_assert_frame_equal.py
    │           │   │   │   ├── test_assert_index_equal.py
    │           │   │   │   ├── test_assert_interval_array_equal.py
    │           │   │   │   ├── test_assert_numpy_array_equal.py
    │           │   │   │   ├── test_assert_produces_warning.py
    │           │   │   │   ├── test_assert_series_equal.py
    │           │   │   │   ├── test_deprecate.py
    │           │   │   │   ├── test_deprecate_kwarg.py
    │           │   │   │   ├── test_deprecate_nonkeyword_arguments.py
    │           │   │   │   ├── test_find_stack_level.py
    │           │   │   │   ├── test_hashing.py
    │           │   │   │   ├── test_numba.py
    │           │   │   │   ├── test_rewrite_warning.py
    │           │   │   │   ├── test_shares_memory.py
    │           │   │   │   ├── test_show_versions.py
    │           │   │   │   ├── test_util.py
    │           │   │   │   ├── test_validate_args.py
    │           │   │   │   ├── test_validate_args_and_kwargs.py
    │           │   │   │   ├── test_validate_inclusive.py
    │           │   │   │   └── test_validate_kwargs.py
    │           │   │   └── window
    │           │   │       ├── __init__.py
    │           │   │       ├── conftest.py
    │           │   │       ├── moments
    │           │   │       │   ├── __init__.py
    │           │   │       │   ├── conftest.py
    │           │   │       │   ├── test_moments_consistency_ewm.py
    │           │   │       │   ├── test_moments_consistency_expanding.py
    │           │   │       │   └── test_moments_consistency_rolling.py
    │           │   │       ├── test_api.py
    │           │   │       ├── test_apply.py
    │           │   │       ├── test_base_indexer.py
    │           │   │       ├── test_cython_aggregations.py
    │           │   │       ├── test_dtypes.py
    │           │   │       ├── test_ewm.py
    │           │   │       ├── test_expanding.py
    │           │   │       ├── test_groupby.py
    │           │   │       ├── test_numba.py
    │           │   │       ├── test_online.py
    │           │   │       ├── test_pairwise.py
    │           │   │       ├── test_rolling.py
    │           │   │       ├── test_rolling_functions.py
    │           │   │       ├── test_rolling_quantile.py
    │           │   │       ├── test_rolling_skew_kurt.py
    │           │   │       ├── test_timeseries_window.py
    │           │   │       └── test_win_type.py
    │           │   ├── tseries
    │           │   │   ├── __init__.py
    │           │   │   ├── api.py
    │           │   │   ├── frequencies.py
    │           │   │   ├── holiday.py
    │           │   │   └── offsets.py
    │           │   └── util
    │           │       ├── __init__.py
    │           │       ├── _decorators.py
    │           │       ├── _doctools.py
    │           │       ├── _exceptions.py
    │           │       ├── _print_versions.py
    │           │       ├── _test_decorators.py
    │           │       ├── _tester.py
    │           │       ├── _validators.py
    │           │       └── version
    │           │           └── __init__.py
    │           ├── pandas-3.1.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       ├── LICENSE
    │           │       ├── LICENSES
    │           │       │   ├── BOTTLENECK_LICENCE
    │           │       │   ├── DATEUTIL_LICENSE
    │           │       │   ├── HAVEN_LICENSE
    │           │       │   ├── HAVEN_MIT
    │           │       │   ├── KLIB_LICENSE
    │           │       │   ├── MUSL_LICENSE
    │           │       │   ├── NUMPY_LICENSE
    │           │       │   ├── PACKAGING_LICENSE
    │           │       │   ├── PSF_LICENSE
    │           │       │   ├── PYPERCLIP_LICENSE
    │           │       │   ├── PYUPGRADE_LICENSE
    │           │       │   ├── SAS7BDAT_LICENSE
    │           │       │   ├── STATSBASE_JL_LICENSE
    │           │       │   ├── ULTRAJSON_LICENSE
    │           │       │   └── XSIMD_LICENSE
    │           │       └── subprojects
    │           │           └── fast_float-8.2.10
    │           │               ├── LICENSE-APACHE
    │           │               ├── LICENSE-BOOST
    │           │               └── LICENSE-MIT
    │           ├── pgvector
    │           │   ├── __init__.py
    │           │   ├── _utils.py
    │           │   ├── asyncpg
    │           │   │   ├── __init__.py
    │           │   │   └── register.py
    │           │   ├── bit.py
    │           │   ├── django
    │           │   │   ├── __init__.py
    │           │   │   ├── bit.py
    │           │   │   ├── extensions.py
    │           │   │   ├── functions.py
    │           │   │   ├── halfvec.py
    │           │   │   ├── indexes.py
    │           │   │   ├── sparsevec.py
    │           │   │   └── vector.py
    │           │   ├── halfvec.py
    │           │   ├── peewee
    │           │   │   ├── __init__.py
    │           │   │   ├── bit.py
    │           │   │   ├── halfvec.py
    │           │   │   ├── sparsevec.py
    │           │   │   └── vector.py
    │           │   ├── pg8000
    │           │   │   ├── __init__.py
    │           │   │   └── register.py
    │           │   ├── psycopg
    │           │   │   ├── __init__.py
    │           │   │   ├── bit.py
    │           │   │   ├── halfvec.py
    │           │   │   ├── register.py
    │           │   │   ├── sparsevec.py
    │           │   │   └── vector.py
    │           │   ├── psycopg2
    │           │   │   ├── __init__.py
    │           │   │   ├── halfvec.py
    │           │   │   ├── register.py
    │           │   │   ├── sparsevec.py
    │           │   │   └── vector.py
    │           │   ├── py.typed
    │           │   ├── sparsevec.py
    │           │   ├── sqlalchemy
    │           │   │   ├── __init__.py
    │           │   │   ├── bit.py
    │           │   │   ├── functions.py
    │           │   │   ├── halfvec.py
    │           │   │   ├── sparsevec.py
    │           │   │   └── vector.py
    │           │   └── vector.py
    │           ├── pgvector-0.5.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── pillow-13.0.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   ├── sboms
    │           │   │   ├── auditwheel.cdx.json
    │           │   │   └── pillow-13.0.0.cdx.json
    │           │   └── top_level.txt
    │           ├── pillow.libs
    │           │   ├── libXau-154567c4.so.6.0.0
    │           │   ├── libavif-c6062d5f.so.16.4.2
    │           │   ├── libbrotlicommon-53534446.so.1.2.0
    │           │   ├── libbrotlidec-7e5462ba.so.1.2.0
    │           │   ├── libfreetype-57f805ba.so.6.20.6
    │           │   ├── libharfbuzz-fb49c9fc.so.0.61450.0
    │           │   ├── libjpeg-6dc8d115.so.62.4.0
    │           │   ├── liblcms2-88eaba2f.so.2.0.19
    │           │   ├── liblzma-de26b416.so.5.8.4
    │           │   ├── libopenjp2-e530e1bf.so.2.5.4
    │           │   ├── libpng16-1d1ba958.so.16.58.0
    │           │   ├── libsharpyuv-0066295b.so.0.1.2
    │           │   ├── libtiff-20b7e810.so.6.3.0
    │           │   ├── libwebp-51b0b3f7.so.7.2.0
    │           │   ├── libwebpdemux-9fe2abcc.so.2.0.17
    │           │   ├── libwebpmux-8fb1c9f6.so.3.1.2
    │           │   ├── libxcb-9065bb12.so.1.1.0
    │           │   └── libzstd-40ad5e7e.so.1.5.7
    │           ├── pip
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── __pip-runner__.py
    │           │   ├── _internal
    │           │   │   ├── __init__.py
    │           │   │   ├── build_env
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── installer.py
    │           │   │   │   ├── noop.py
    │           │   │   │   ├── venv.py
    │           │   │   │   └── virtual.py
    │           │   │   ├── cache.py
    │           │   │   ├── cli
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── autocompletion.py
    │           │   │   │   ├── base_command.py
    │           │   │   │   ├── cmdoptions.py
    │           │   │   │   ├── command_context.py
    │           │   │   │   ├── index_command.py
    │           │   │   │   ├── main.py
    │           │   │   │   ├── main_parser.py
    │           │   │   │   ├── parser.py
    │           │   │   │   ├── progress_bars.py
    │           │   │   │   ├── req_command.py
    │           │   │   │   ├── spinners.py
    │           │   │   │   └── status_codes.py
    │           │   │   ├── commands
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── cache.py
    │           │   │   │   ├── check.py
    │           │   │   │   ├── completion.py
    │           │   │   │   ├── configuration.py
    │           │   │   │   ├── debug.py
    │           │   │   │   ├── download.py
    │           │   │   │   ├── freeze.py
    │           │   │   │   ├── hash.py
    │           │   │   │   ├── help.py
    │           │   │   │   ├── index.py
    │           │   │   │   ├── inspect.py
    │           │   │   │   ├── install.py
    │           │   │   │   ├── list.py
    │           │   │   │   ├── lock.py
    │           │   │   │   ├── search.py
    │           │   │   │   ├── show.py
    │           │   │   │   ├── uninstall.py
    │           │   │   │   └── wheel.py
    │           │   │   ├── configuration.py
    │           │   │   ├── distributions
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── installed.py
    │           │   │   │   ├── sdist.py
    │           │   │   │   └── wheel.py
    │           │   │   ├── exceptions
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _base.py
    │           │   │   │   ├── build.py
    │           │   │   │   ├── hashes.py
    │           │   │   │   ├── network.py
    │           │   │   │   ├── pyproject.py
    │           │   │   │   ├── uninstall.py
    │           │   │   │   └── wheel.py
    │           │   │   ├── index
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── collector.py
    │           │   │   │   ├── package_finder.py
    │           │   │   │   └── sources.py
    │           │   │   ├── locations
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _distutils.py
    │           │   │   │   ├── _sysconfig.py
    │           │   │   │   └── base.py
    │           │   │   ├── main.py
    │           │   │   ├── metadata
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _json.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── direct_references.py
    │           │   │   │   ├── importlib
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── _compat.py
    │           │   │   │   │   ├── _dists.py
    │           │   │   │   │   └── _envs.py
    │           │   │   │   └── pkg_resources.py
    │           │   │   ├── models
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── candidate.py
    │           │   │   │   ├── direct_url.py
    │           │   │   │   ├── format_control.py
    │           │   │   │   ├── index.py
    │           │   │   │   ├── installation_report.py
    │           │   │   │   ├── link.py
    │           │   │   │   ├── release_control.py
    │           │   │   │   ├── scheme.py
    │           │   │   │   ├── search_scope.py
    │           │   │   │   ├── selection_prefs.py
    │           │   │   │   ├── target_python.py
    │           │   │   │   └── wheel.py
    │           │   │   ├── network
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── auth.py
    │           │   │   │   ├── cache.py
    │           │   │   │   ├── download.py
    │           │   │   │   ├── lazy_wheel.py
    │           │   │   │   ├── session.py
    │           │   │   │   ├── utils.py
    │           │   │   │   └── xmlrpc.py
    │           │   │   ├── operations
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── check.py
    │           │   │   │   ├── freeze.py
    │           │   │   │   ├── install
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── wheel.py
    │           │   │   │   └── prepare.py
    │           │   │   ├── pyproject.py
    │           │   │   ├── req
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── constructors.py
    │           │   │   │   ├── pep723.py
    │           │   │   │   ├── req_dependency_group.py
    │           │   │   │   ├── req_file.py
    │           │   │   │   ├── req_install.py
    │           │   │   │   ├── req_set.py
    │           │   │   │   └── req_uninstall.py
    │           │   │   ├── resolution
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── legacy
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── resolver.py
    │           │   │   │   └── resolvelib
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── base.py
    │           │   │   │       ├── candidates.py
    │           │   │   │       ├── factory.py
    │           │   │   │       ├── found_candidates.py
    │           │   │   │       ├── provider.py
    │           │   │   │       ├── reporter.py
    │           │   │   │       ├── requirements.py
    │           │   │   │       └── resolver.py
    │           │   │   ├── self_outdated_check.py
    │           │   │   ├── utils
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _jaraco_text.py
    │           │   │   │   ├── _log.py
    │           │   │   │   ├── appdirs.py
    │           │   │   │   ├── compat.py
    │           │   │   │   ├── compatibility_tags.py
    │           │   │   │   ├── datetime.py
    │           │   │   │   ├── deprecation.py
    │           │   │   │   ├── direct_url_helpers.py
    │           │   │   │   ├── egg_link.py
    │           │   │   │   ├── entrypoints.py
    │           │   │   │   ├── filesystem.py
    │           │   │   │   ├── filetypes.py
    │           │   │   │   ├── glibc.py
    │           │   │   │   ├── hashes.py
    │           │   │   │   ├── logging.py
    │           │   │   │   ├── misc.py
    │           │   │   │   ├── packaging.py
    │           │   │   │   ├── pylock.py
    │           │   │   │   ├── retry.py
    │           │   │   │   ├── subprocess.py
    │           │   │   │   ├── temp_dir.py
    │           │   │   │   ├── unpacking.py
    │           │   │   │   ├── urls.py
    │           │   │   │   ├── virtualenv.py
    │           │   │   │   └── wheel.py
    │           │   │   ├── vcs
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── bazaar.py
    │           │   │   │   ├── git.py
    │           │   │   │   ├── mercurial.py
    │           │   │   │   ├── subversion.py
    │           │   │   │   └── versioncontrol.py
    │           │   │   └── wheel_builder.py
    │           │   ├── _vendor
    │           │   │   ├── README.rst
    │           │   │   ├── __init__.py
    │           │   │   ├── bom.cdx.json
    │           │   │   ├── cachecontrol
    │           │   │   │   ├── LICENSE.txt
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _cmd.py
    │           │   │   │   ├── adapter.py
    │           │   │   │   ├── cache.py
    │           │   │   │   ├── caches
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── file_cache.py
    │           │   │   │   │   └── redis_cache.py
    │           │   │   │   ├── controller.py
    │           │   │   │   ├── filewrapper.py
    │           │   │   │   ├── heuristics.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── serialize.py
    │           │   │   │   └── wrapper.py
    │           │   │   ├── certifi
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __main__.py
    │           │   │   │   ├── cacert.pem
    │           │   │   │   ├── core.py
    │           │   │   │   ├── py.typed
    │           │   │   │   └── tests
    │           │   │   │       ├── __init__.py
    │           │   │   │       └── test_certify.py
    │           │   │   ├── distlib
    │           │   │   │   ├── LICENSE.txt
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── compat.py
    │           │   │   │   ├── resources.py
    │           │   │   │   ├── scripts.py
    │           │   │   │   ├── t32.exe
    │           │   │   │   ├── t64-arm.exe
    │           │   │   │   ├── t64.exe
    │           │   │   │   ├── util.py
    │           │   │   │   ├── w32.exe
    │           │   │   │   ├── w64-arm.exe
    │           │   │   │   └── w64.exe
    │           │   │   ├── distro
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __main__.py
    │           │   │   │   ├── distro.py
    │           │   │   │   └── py.typed
    │           │   │   ├── idna
    │           │   │   │   ├── LICENSE.md
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __main__.py
    │           │   │   │   ├── cli.py
    │           │   │   │   ├── codec.py
    │           │   │   │   ├── compat.py
    │           │   │   │   ├── core.py
    │           │   │   │   ├── idnadata.py
    │           │   │   │   ├── intranges.py
    │           │   │   │   ├── package_data.py
    │           │   │   │   ├── py.typed
    │           │   │   │   └── uts46data.py
    │           │   │   ├── msgpack
    │           │   │   │   ├── COPYING
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── exceptions.py
    │           │   │   │   ├── ext.py
    │           │   │   │   └── fallback.py
    │           │   │   ├── packaging
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── LICENSE.APACHE
    │           │   │   │   ├── LICENSE.BSD
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _elffile.py
    │           │   │   │   ├── _manylinux.py
    │           │   │   │   ├── _musllinux.py
    │           │   │   │   ├── _parser.py
    │           │   │   │   ├── _ranges.py
    │           │   │   │   ├── _structures.py
    │           │   │   │   ├── _tokenizer.py
    │           │   │   │   ├── dependency_groups.py
    │           │   │   │   ├── direct_url.py
    │           │   │   │   ├── errors.py
    │           │   │   │   ├── licenses
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── _spdx.py
    │           │   │   │   ├── markers.py
    │           │   │   │   ├── metadata.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── pylock.py
    │           │   │   │   ├── ranges.py
    │           │   │   │   ├── requirements.py
    │           │   │   │   ├── specifiers.py
    │           │   │   │   ├── tags.py
    │           │   │   │   ├── utils.py
    │           │   │   │   └── version.py
    │           │   │   ├── pkg_resources
    │           │   │   │   ├── LICENSE
    │           │   │   │   └── __init__.py
    │           │   │   ├── platformdirs
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __main__.py
    │           │   │   │   ├── _xdg.py
    │           │   │   │   ├── android.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── ios.py
    │           │   │   │   ├── macos.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── pytest_plugin.py
    │           │   │   │   ├── testing.py
    │           │   │   │   ├── unix.py
    │           │   │   │   ├── version.py
    │           │   │   │   └── windows.py
    │           │   │   ├── pygments
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __main__.py
    │           │   │   │   ├── console.py
    │           │   │   │   ├── filter.py
    │           │   │   │   ├── filters
    │           │   │   │   │   └── __init__.py
    │           │   │   │   ├── formatter.py
    │           │   │   │   ├── formatters
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── _mapping.py
    │           │   │   │   ├── lexer.py
    │           │   │   │   ├── lexers
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── _mapping.py
    │           │   │   │   │   └── python.py
    │           │   │   │   ├── modeline.py
    │           │   │   │   ├── plugin.py
    │           │   │   │   ├── regexopt.py
    │           │   │   │   ├── scanner.py
    │           │   │   │   ├── sphinxext.py
    │           │   │   │   ├── style.py
    │           │   │   │   ├── styles
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── _mapping.py
    │           │   │   │   ├── token.py
    │           │   │   │   ├── unistring.py
    │           │   │   │   └── util.py
    │           │   │   ├── pyproject_hooks
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _impl.py
    │           │   │   │   ├── _in_process
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   └── _in_process.py
    │           │   │   │   └── py.typed
    │           │   │   ├── requests
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __version__.py
    │           │   │   │   ├── _internal_utils.py
    │           │   │   │   ├── _types.py
    │           │   │   │   ├── adapters.py
    │           │   │   │   ├── api.py
    │           │   │   │   ├── auth.py
    │           │   │   │   ├── certs.py
    │           │   │   │   ├── compat.py
    │           │   │   │   ├── cookies.py
    │           │   │   │   ├── exceptions.py
    │           │   │   │   ├── help.py
    │           │   │   │   ├── hooks.py
    │           │   │   │   ├── models.py
    │           │   │   │   ├── packages.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── sessions.py
    │           │   │   │   ├── status_codes.py
    │           │   │   │   ├── structures.py
    │           │   │   │   └── utils.py
    │           │   │   ├── resolvelib
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── providers.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── reporters.py
    │           │   │   │   ├── resolvers
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── abstract.py
    │           │   │   │   │   ├── criterion.py
    │           │   │   │   │   ├── exceptions.py
    │           │   │   │   │   └── resolution.py
    │           │   │   │   └── structs.py
    │           │   │   ├── rich
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── __main__.py
    │           │   │   │   ├── _emoji_codes.py
    │           │   │   │   ├── _emoji_replace.py
    │           │   │   │   ├── _export_format.py
    │           │   │   │   ├── _extension.py
    │           │   │   │   ├── _fileno.py
    │           │   │   │   ├── _inspect.py
    │           │   │   │   ├── _log_render.py
    │           │   │   │   ├── _loop.py
    │           │   │   │   ├── _null_file.py
    │           │   │   │   ├── _palettes.py
    │           │   │   │   ├── _pick.py
    │           │   │   │   ├── _ratio.py
    │           │   │   │   ├── _spinners.py
    │           │   │   │   ├── _stack.py
    │           │   │   │   ├── _timer.py
    │           │   │   │   ├── _unicode_data
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── _versions.py
    │           │   │   │   │   ├── unicode10-0-0.py
    │           │   │   │   │   ├── unicode11-0-0.py
    │           │   │   │   │   ├── unicode12-0-0.py
    │           │   │   │   │   ├── unicode12-1-0.py
    │           │   │   │   │   ├── unicode13-0-0.py
    │           │   │   │   │   ├── unicode14-0-0.py
    │           │   │   │   │   ├── unicode15-0-0.py
    │           │   │   │   │   ├── unicode15-1-0.py
    │           │   │   │   │   ├── unicode16-0-0.py
    │           │   │   │   │   ├── unicode17-0-0.py
    │           │   │   │   │   ├── unicode4-1-0.py
    │           │   │   │   │   ├── unicode5-0-0.py
    │           │   │   │   │   ├── unicode5-1-0.py
    │           │   │   │   │   ├── unicode5-2-0.py
    │           │   │   │   │   ├── unicode6-0-0.py
    │           │   │   │   │   ├── unicode6-1-0.py
    │           │   │   │   │   ├── unicode6-2-0.py
    │           │   │   │   │   ├── unicode6-3-0.py
    │           │   │   │   │   ├── unicode7-0-0.py
    │           │   │   │   │   ├── unicode8-0-0.py
    │           │   │   │   │   └── unicode9-0-0.py
    │           │   │   │   ├── _win32_console.py
    │           │   │   │   ├── _windows.py
    │           │   │   │   ├── _windows_renderer.py
    │           │   │   │   ├── _wrap.py
    │           │   │   │   ├── abc.py
    │           │   │   │   ├── align.py
    │           │   │   │   ├── ansi.py
    │           │   │   │   ├── bar.py
    │           │   │   │   ├── box.py
    │           │   │   │   ├── cells.py
    │           │   │   │   ├── color.py
    │           │   │   │   ├── color_triplet.py
    │           │   │   │   ├── columns.py
    │           │   │   │   ├── console.py
    │           │   │   │   ├── constrain.py
    │           │   │   │   ├── containers.py
    │           │   │   │   ├── control.py
    │           │   │   │   ├── default_styles.py
    │           │   │   │   ├── diagnose.py
    │           │   │   │   ├── emoji.py
    │           │   │   │   ├── errors.py
    │           │   │   │   ├── file_proxy.py
    │           │   │   │   ├── filesize.py
    │           │   │   │   ├── highlighter.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── jupyter.py
    │           │   │   │   ├── layout.py
    │           │   │   │   ├── live.py
    │           │   │   │   ├── live_render.py
    │           │   │   │   ├── logging.py
    │           │   │   │   ├── markup.py
    │           │   │   │   ├── measure.py
    │           │   │   │   ├── padding.py
    │           │   │   │   ├── pager.py
    │           │   │   │   ├── palette.py
    │           │   │   │   ├── panel.py
    │           │   │   │   ├── pretty.py
    │           │   │   │   ├── progress.py
    │           │   │   │   ├── progress_bar.py
    │           │   │   │   ├── prompt.py
    │           │   │   │   ├── protocol.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── region.py
    │           │   │   │   ├── repr.py
    │           │   │   │   ├── rule.py
    │           │   │   │   ├── scope.py
    │           │   │   │   ├── screen.py
    │           │   │   │   ├── segment.py
    │           │   │   │   ├── spinner.py
    │           │   │   │   ├── status.py
    │           │   │   │   ├── style.py
    │           │   │   │   ├── styled.py
    │           │   │   │   ├── syntax.py
    │           │   │   │   ├── table.py
    │           │   │   │   ├── terminal_theme.py
    │           │   │   │   ├── text.py
    │           │   │   │   ├── theme.py
    │           │   │   │   ├── themes.py
    │           │   │   │   ├── traceback.py
    │           │   │   │   └── tree.py
    │           │   │   ├── tomli
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _parser.py
    │           │   │   │   ├── _re.py
    │           │   │   │   ├── _types.py
    │           │   │   │   └── py.typed
    │           │   │   ├── tomli_w
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _writer.py
    │           │   │   │   └── py.typed
    │           │   │   ├── truststore
    │           │   │   │   ├── LICENSE
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _api.py
    │           │   │   │   ├── _macos.py
    │           │   │   │   ├── _openssl.py
    │           │   │   │   ├── _ssl_constants.py
    │           │   │   │   ├── _windows.py
    │           │   │   │   └── py.typed
    │           │   │   ├── urllib3
    │           │   │   │   ├── LICENSE.txt
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _base_connection.py
    │           │   │   │   ├── _collections.py
    │           │   │   │   ├── _request_methods.py
    │           │   │   │   ├── _version.py
    │           │   │   │   ├── connection.py
    │           │   │   │   ├── connectionpool.py
    │           │   │   │   ├── contrib
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── emscripten
    │           │   │   │   │   │   ├── __init__.py
    │           │   │   │   │   │   ├── connection.py
    │           │   │   │   │   │   ├── emscripten_fetch_worker.js
    │           │   │   │   │   │   ├── fetch.py
    │           │   │   │   │   │   ├── request.py
    │           │   │   │   │   │   └── response.py
    │           │   │   │   │   ├── pyopenssl.py
    │           │   │   │   │   └── socks.py
    │           │   │   │   ├── exceptions.py
    │           │   │   │   ├── fields.py
    │           │   │   │   ├── filepost.py
    │           │   │   │   ├── http2
    │           │   │   │   │   ├── __init__.py
    │           │   │   │   │   ├── connection.py
    │           │   │   │   │   └── probe.py
    │           │   │   │   ├── poolmanager.py
    │           │   │   │   ├── py.typed
    │           │   │   │   ├── response.py
    │           │   │   │   └── util
    │           │   │   │       ├── __init__.py
    │           │   │   │       ├── connection.py
    │           │   │   │       ├── proxy.py
    │           │   │   │       ├── request.py
    │           │   │   │       ├── response.py
    │           │   │   │       ├── retry.py
    │           │   │   │       ├── ssl_.py
    │           │   │   │       ├── ssl_match_hostname.py
    │           │   │   │       ├── ssltransport.py
    │           │   │   │       ├── timeout.py
    │           │   │   │       ├── url.py
    │           │   │   │       ├── util.py
    │           │   │   │       └── wait.py
    │           │   │   └── vendor.txt
    │           │   └── py.typed
    │           ├── pip-26.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       ├── AUTHORS.txt
    │           │       ├── LICENSE.txt
    │           │       └── src
    │           │           └── pip
    │           │               └── _vendor
    │           │                   ├── cachecontrol
    │           │                   │   └── LICENSE.txt
    │           │                   ├── certifi
    │           │                   │   └── LICENSE
    │           │                   ├── distlib
    │           │                   │   └── LICENSE.txt
    │           │                   ├── distro
    │           │                   │   └── LICENSE
    │           │                   ├── idna
    │           │                   │   └── LICENSE.md
    │           │                   ├── msgpack
    │           │                   │   └── COPYING
    │           │                   ├── packaging
    │           │                   │   ├── LICENSE
    │           │                   │   ├── LICENSE.APACHE
    │           │                   │   └── LICENSE.BSD
    │           │                   ├── pkg_resources
    │           │                   │   └── LICENSE
    │           │                   ├── platformdirs
    │           │                   │   └── LICENSE
    │           │                   ├── pygments
    │           │                   │   └── LICENSE
    │           │                   ├── pyproject_hooks
    │           │                   │   └── LICENSE
    │           │                   ├── requests
    │           │                   │   └── LICENSE
    │           │                   ├── resolvelib
    │           │                   │   └── LICENSE
    │           │                   ├── rich
    │           │                   │   └── LICENSE
    │           │                   ├── tomli
    │           │                   │   └── LICENSE
    │           │                   ├── tomli_w
    │           │                   │   └── LICENSE
    │           │                   ├── truststore
    │           │                   │   └── LICENSE
    │           │                   └── urllib3
    │           │                       └── LICENSE.txt
    │           ├── pluggy
    │           │   ├── __init__.py
    │           │   ├── _caller.py
    │           │   ├── _callers.py
    │           │   ├── _compat.py
    │           │   ├── _config.py
    │           │   ├── _decorators.py
    │           │   ├── _execution.py
    │           │   ├── _hooks.py
    │           │   ├── _impl.py
    │           │   ├── _manager.py
    │           │   ├── _result.py
    │           │   ├── _tracing.py
    │           │   ├── _warnings.py
    │           │   └── py.typed
    │           ├── pluggy-1.7.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── prompt_toolkit
    │           │   ├── __init__.py
    │           │   ├── application
    │           │   │   ├── __init__.py
    │           │   │   ├── application.py
    │           │   │   ├── current.py
    │           │   │   ├── dummy.py
    │           │   │   └── run_in_terminal.py
    │           │   ├── auto_suggest.py
    │           │   ├── buffer.py
    │           │   ├── cache.py
    │           │   ├── clipboard
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── in_memory.py
    │           │   │   └── pyperclip.py
    │           │   ├── completion
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── deduplicate.py
    │           │   │   ├── filesystem.py
    │           │   │   ├── fuzzy_completer.py
    │           │   │   ├── nested.py
    │           │   │   └── word_completer.py
    │           │   ├── contrib
    │           │   │   ├── __init__.py
    │           │   │   ├── completers
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── system.py
    │           │   │   ├── regular_languages
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── compiler.py
    │           │   │   │   ├── completion.py
    │           │   │   │   ├── lexer.py
    │           │   │   │   ├── regex_parser.py
    │           │   │   │   └── validation.py
    │           │   │   ├── ssh
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── server.py
    │           │   │   └── telnet
    │           │   │       ├── __init__.py
    │           │   │       ├── log.py
    │           │   │       ├── protocol.py
    │           │   │       └── server.py
    │           │   ├── cursor_shapes.py
    │           │   ├── data_structures.py
    │           │   ├── document.py
    │           │   ├── enums.py
    │           │   ├── eventloop
    │           │   │   ├── __init__.py
    │           │   │   ├── async_generator.py
    │           │   │   ├── inputhook.py
    │           │   │   ├── utils.py
    │           │   │   └── win32.py
    │           │   ├── filters
    │           │   │   ├── __init__.py
    │           │   │   ├── app.py
    │           │   │   ├── base.py
    │           │   │   ├── cli.py
    │           │   │   └── utils.py
    │           │   ├── formatted_text
    │           │   │   ├── __init__.py
    │           │   │   ├── ansi.py
    │           │   │   ├── base.py
    │           │   │   ├── html.py
    │           │   │   ├── pygments.py
    │           │   │   └── utils.py
    │           │   ├── history.py
    │           │   ├── input
    │           │   │   ├── __init__.py
    │           │   │   ├── ansi_escape_sequences.py
    │           │   │   ├── base.py
    │           │   │   ├── defaults.py
    │           │   │   ├── posix_pipe.py
    │           │   │   ├── posix_utils.py
    │           │   │   ├── typeahead.py
    │           │   │   ├── vt100.py
    │           │   │   ├── vt100_parser.py
    │           │   │   ├── win32.py
    │           │   │   └── win32_pipe.py
    │           │   ├── key_binding
    │           │   │   ├── __init__.py
    │           │   │   ├── bindings
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── auto_suggest.py
    │           │   │   │   ├── basic.py
    │           │   │   │   ├── completion.py
    │           │   │   │   ├── cpr.py
    │           │   │   │   ├── emacs.py
    │           │   │   │   ├── focus.py
    │           │   │   │   ├── mouse.py
    │           │   │   │   ├── named_commands.py
    │           │   │   │   ├── open_in_editor.py
    │           │   │   │   ├── page_navigation.py
    │           │   │   │   ├── scroll.py
    │           │   │   │   ├── search.py
    │           │   │   │   └── vi.py
    │           │   │   ├── defaults.py
    │           │   │   ├── digraphs.py
    │           │   │   ├── emacs_state.py
    │           │   │   ├── key_bindings.py
    │           │   │   ├── key_processor.py
    │           │   │   └── vi_state.py
    │           │   ├── keys.py
    │           │   ├── layout
    │           │   │   ├── __init__.py
    │           │   │   ├── containers.py
    │           │   │   ├── controls.py
    │           │   │   ├── dimension.py
    │           │   │   ├── dummy.py
    │           │   │   ├── layout.py
    │           │   │   ├── margins.py
    │           │   │   ├── menus.py
    │           │   │   ├── mouse_handlers.py
    │           │   │   ├── processors.py
    │           │   │   ├── screen.py
    │           │   │   ├── scrollable_pane.py
    │           │   │   └── utils.py
    │           │   ├── lexers
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   └── pygments.py
    │           │   ├── log.py
    │           │   ├── mouse_events.py
    │           │   ├── output
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── color_depth.py
    │           │   │   ├── conemu.py
    │           │   │   ├── defaults.py
    │           │   │   ├── flush_stdout.py
    │           │   │   ├── plain_text.py
    │           │   │   ├── vt100.py
    │           │   │   ├── win32.py
    │           │   │   └── windows10.py
    │           │   ├── patch_stdout.py
    │           │   ├── py.typed
    │           │   ├── renderer.py
    │           │   ├── search.py
    │           │   ├── selection.py
    │           │   ├── shortcuts
    │           │   │   ├── __init__.py
    │           │   │   ├── choice_input.py
    │           │   │   ├── dialogs.py
    │           │   │   ├── progress_bar
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   └── formatters.py
    │           │   │   ├── prompt.py
    │           │   │   └── utils.py
    │           │   ├── styles
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── defaults.py
    │           │   │   ├── named_colors.py
    │           │   │   ├── pygments.py
    │           │   │   ├── style.py
    │           │   │   └── style_transformation.py
    │           │   ├── token.py
    │           │   ├── utils.py
    │           │   ├── validation.py
    │           │   ├── widgets
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── dialogs.py
    │           │   │   ├── menus.py
    │           │   │   └── toolbars.py
    │           │   └── win32_types.py
    │           ├── prompt_toolkit-3.0.53.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── AUTHORS.rst
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── protobuf-7.36.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   └── WHEEL
    │           ├── psutil
    │           │   ├── __init__.py
    │           │   ├── _common.py
    │           │   ├── _ntuples.py
    │           │   ├── _psaix.py
    │           │   ├── _psbsd.py
    │           │   ├── _pslinux.py
    │           │   ├── _psosx.py
    │           │   ├── _psposix.py
    │           │   ├── _pssunos.py
    │           │   ├── _psutil_linux.abi3.so
    │           │   └── _pswindows.py
    │           ├── psutil-7.2.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── psycopg
    │           │   ├── __init__.py
    │           │   ├── _acompat.py
    │           │   ├── _adapters_map.py
    │           │   ├── _capabilities.py
    │           │   ├── _cmodule.py
    │           │   ├── _column.py
    │           │   ├── _compat.py
    │           │   ├── _connection_base.py
    │           │   ├── _connection_info.py
    │           │   ├── _conninfo_attempts.py
    │           │   ├── _conninfo_attempts_async.py
    │           │   ├── _conninfo_utils.py
    │           │   ├── _copy.py
    │           │   ├── _copy_async.py
    │           │   ├── _copy_base.py
    │           │   ├── _cursor_base.py
    │           │   ├── _dns.py
    │           │   ├── _encodings.py
    │           │   ├── _enums.py
    │           │   ├── _oids.py
    │           │   ├── _pipeline.py
    │           │   ├── _pipeline_async.py
    │           │   ├── _pipeline_base.py
    │           │   ├── _preparing.py
    │           │   ├── _py_transformer.py
    │           │   ├── _queries.py
    │           │   ├── _server_cursor.py
    │           │   ├── _server_cursor_async.py
    │           │   ├── _server_cursor_base.py
    │           │   ├── _struct.py
    │           │   ├── _tpc.py
    │           │   ├── _transformer.py
    │           │   ├── _tstrings.py
    │           │   ├── _typeinfo.py
    │           │   ├── _typemod.py
    │           │   ├── _tz.py
    │           │   ├── _wrappers.py
    │           │   ├── abc.py
    │           │   ├── adapt.py
    │           │   ├── client_cursor.py
    │           │   ├── connection.py
    │           │   ├── connection_async.py
    │           │   ├── conninfo.py
    │           │   ├── copy.py
    │           │   ├── crdb
    │           │   │   ├── __init__.py
    │           │   │   ├── _types.py
    │           │   │   └── connection.py
    │           │   ├── cursor.py
    │           │   ├── cursor_async.py
    │           │   ├── dbapi20.py
    │           │   ├── errors.py
    │           │   ├── generators.py
    │           │   ├── postgres.py
    │           │   ├── pq
    │           │   │   ├── __init__.py
    │           │   │   ├── _debug.py
    │           │   │   ├── _enums.py
    │           │   │   ├── _pq_ctypes.py
    │           │   │   ├── _pq_ctypes.pyi
    │           │   │   ├── abc.py
    │           │   │   ├── misc.py
    │           │   │   └── pq_ctypes.py
    │           │   ├── py.typed
    │           │   ├── raw_cursor.py
    │           │   ├── rows.py
    │           │   ├── sql.py
    │           │   ├── transaction.py
    │           │   ├── types
    │           │   │   ├── __init__.py
    │           │   │   ├── array.py
    │           │   │   ├── bool.py
    │           │   │   ├── composite.py
    │           │   │   ├── datetime.py
    │           │   │   ├── enum.py
    │           │   │   ├── hstore.py
    │           │   │   ├── json.py
    │           │   │   ├── multirange.py
    │           │   │   ├── net.py
    │           │   │   ├── none.py
    │           │   │   ├── numeric.py
    │           │   │   ├── numpy.py
    │           │   │   ├── range.py
    │           │   │   ├── shapely.py
    │           │   │   ├── string.py
    │           │   │   └── uuid.py
    │           │   ├── version.py
    │           │   └── waiting.py
    │           ├── psycopg-3.3.9.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── psycopg2
    │           │   ├── __init__.py
    │           │   ├── _ipaddress.py
    │           │   ├── _json.py
    │           │   ├── _psycopg.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _range.py
    │           │   ├── errorcodes.py
    │           │   ├── errors.py
    │           │   ├── extensions.py
    │           │   ├── extras.py
    │           │   ├── pool.py
    │           │   ├── sql.py
    │           │   └── tz.py
    │           ├── psycopg2_binary-2.9.13.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   ├── sboms
    │           │   │   └── auditwheel.cdx.json
    │           │   └── top_level.txt
    │           ├── psycopg2_binary.libs
    │           │   ├── libcom_err-2abe824b.so.2.1
    │           │   ├── libcrypt-bc2db45e.so.1
    │           │   ├── libcrypto-fb8d5b21.so.3
    │           │   ├── libgssapi_krb5-497db0c6.so.2.2
    │           │   ├── libk5crypto-b1f99d5c.so.3.1
    │           │   ├── libkeyutils-dfe70bd6.so.1.5
    │           │   ├── libkrb5-fcafa220.so.3.3
    │           │   ├── libkrb5support-d0bcff84.so.0.1
    │           │   ├── liblber-2f335fb0.so.2.0.200
    │           │   ├── libldap-d3931cbf.so.2.0.200
    │           │   ├── libpcre-9513aab5.so.1.2.0
    │           │   ├── libpq-a17e3caa.so.5.17
    │           │   ├── libsasl2-84219a89.so.3.0.0
    │           │   ├── libselinux-0922c95c.so.1
    │           │   └── libssl-8bd944e8.so.3
    │           ├── psycopg_binary
    │           │   ├── __init__.py
    │           │   ├── _psycopg.cpython-314-x86_64-linux-gnu.so
    │           │   ├── _psycopg.pyi
    │           │   ├── pq.cpython-314-x86_64-linux-gnu.so
    │           │   ├── py.typed
    │           │   └── version.py
    │           ├── psycopg_binary-3.3.9.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   ├── sboms
    │           │   │   └── auditwheel.cdx.json
    │           │   └── top_level.txt
    │           ├── psycopg_binary.libs
    │           │   ├── libcom_err-2abe824b.so.2.1
    │           │   ├── libcom_err-55c5739a.so.3.0
    │           │   ├── libcrypt-bc2db45e.so.1
    │           │   ├── libcrypto-3a0647ea.so.3
    │           │   ├── libgssapi_krb5-923083ce.so.2.2
    │           │   ├── libk5crypto-459efceb.so.3.1
    │           │   ├── libkeyutils-dfe70bd6.so.1.5
    │           │   ├── libkrb5-f18b4d11.so.3.3
    │           │   ├── libkrb5support-93fbab13.so.0.1
    │           │   ├── liblber-7b3e3cc5.so.2.0.200
    │           │   ├── libldap-fb847fea.so.2.0.200
    │           │   ├── libpq-e9b5c9ac.so.5.18
    │           │   ├── libsasl2-84219a89.so.3.0.0
    │           │   └── libssl-6a9b88ec.so.3
    │           ├── py.py
    │           ├── py_rust_stemmers
    │           │   ├── __init__.py
    │           │   └── py_rust_stemmers.cpython-314-x86_64-linux-gnu.so
    │           ├── py_rust_stemmers-0.1.8.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── sboms
    │           │       └── py_rust_stemmers.cyclonedx.json
    │           ├── pydantic
    │           │   ├── __init__.py
    │           │   ├── _internal
    │           │   │   ├── __init__.py
    │           │   │   ├── _config.py
    │           │   │   ├── _contextlib.py
    │           │   │   ├── _core_metadata.py
    │           │   │   ├── _core_utils.py
    │           │   │   ├── _dataclasses.py
    │           │   │   ├── _decorators.py
    │           │   │   ├── _decorators_v1.py
    │           │   │   ├── _discriminated_union.py
    │           │   │   ├── _docs_extraction.py
    │           │   │   ├── _fields.py
    │           │   │   ├── _forward_ref.py
    │           │   │   ├── _generate_schema.py
    │           │   │   ├── _generics.py
    │           │   │   ├── _git.py
    │           │   │   ├── _import_utils.py
    │           │   │   ├── _known_annotated_metadata.py
    │           │   │   ├── _mock_val_ser.py
    │           │   │   ├── _model_construction.py
    │           │   │   ├── _namespace_utils.py
    │           │   │   ├── _repr.py
    │           │   │   ├── _schema_gather.py
    │           │   │   ├── _schema_generation_shared.py
    │           │   │   ├── _serializers.py
    │           │   │   ├── _signature.py
    │           │   │   ├── _type_refs.py
    │           │   │   ├── _typing_extra.py
    │           │   │   ├── _utils.py
    │           │   │   ├── _validate_call.py
    │           │   │   └── _validators.py
    │           │   ├── _migration.py
    │           │   ├── alias_generators.py
    │           │   ├── aliases.py
    │           │   ├── annotated_handlers.py
    │           │   ├── class_validators.py
    │           │   ├── color.py
    │           │   ├── config.py
    │           │   ├── dataclasses.py
    │           │   ├── datetime_parse.py
    │           │   ├── decorator.py
    │           │   ├── deprecated
    │           │   │   ├── __init__.py
    │           │   │   ├── class_validators.py
    │           │   │   ├── config.py
    │           │   │   ├── copy_internals.py
    │           │   │   ├── decorator.py
    │           │   │   ├── json.py
    │           │   │   ├── parse.py
    │           │   │   └── tools.py
    │           │   ├── env_settings.py
    │           │   ├── error_wrappers.py
    │           │   ├── errors.py
    │           │   ├── experimental
    │           │   │   ├── __init__.py
    │           │   │   ├── arguments_schema.py
    │           │   │   ├── missing_sentinel.py
    │           │   │   └── pipeline.py
    │           │   ├── fields.py
    │           │   ├── functional_serializers.py
    │           │   ├── functional_validators.py
    │           │   ├── generics.py
    │           │   ├── json.py
    │           │   ├── json_schema.py
    │           │   ├── main.py
    │           │   ├── mypy.py
    │           │   ├── networks.py
    │           │   ├── parse.py
    │           │   ├── plugin
    │           │   │   ├── __init__.py
    │           │   │   ├── _loader.py
    │           │   │   └── _schema_validator.py
    │           │   ├── py.typed
    │           │   ├── root_model.py
    │           │   ├── schema.py
    │           │   ├── tools.py
    │           │   ├── type_adapter.py
    │           │   ├── types.py
    │           │   ├── typing.py
    │           │   ├── utils.py
    │           │   ├── v1
    │           │   │   ├── __init__.py
    │           │   │   ├── _hypothesis_plugin.py
    │           │   │   ├── annotated_types.py
    │           │   │   ├── class_validators.py
    │           │   │   ├── color.py
    │           │   │   ├── config.py
    │           │   │   ├── dataclasses.py
    │           │   │   ├── datetime_parse.py
    │           │   │   ├── decorator.py
    │           │   │   ├── env_settings.py
    │           │   │   ├── error_wrappers.py
    │           │   │   ├── errors.py
    │           │   │   ├── fields.py
    │           │   │   ├── generics.py
    │           │   │   ├── json.py
    │           │   │   ├── main.py
    │           │   │   ├── mypy.py
    │           │   │   ├── networks.py
    │           │   │   ├── parse.py
    │           │   │   ├── py.typed
    │           │   │   ├── schema.py
    │           │   │   ├── tools.py
    │           │   │   ├── types.py
    │           │   │   ├── typing.py
    │           │   │   ├── utils.py
    │           │   │   ├── validators.py
    │           │   │   └── version.py
    │           │   ├── validate_call_decorator.py
    │           │   ├── validators.py
    │           │   ├── version.py
    │           │   └── warnings.py
    │           ├── pydantic-2.14.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── pydantic_core
    │           │   ├── __init__.py
    │           │   ├── _pydantic_core
    │           │   │   ├── __init__.pyi
    │           │   │   └── _schema_gather.pyi
    │           │   ├── _pydantic_core.cpython-314-x86_64-linux-gnu.so
    │           │   ├── core_schema.py
    │           │   └── py.typed
    │           ├── pydantic_core-2.50.4.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── sboms
    │           │       └── pydantic-core.cyclonedx.json
    │           ├── pydantic_settings
    │           │   ├── __init__.py
    │           │   ├── exceptions.py
    │           │   ├── main.py
    │           │   ├── py.typed
    │           │   ├── sources
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── providers
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── aws.py
    │           │   │   │   ├── azure.py
    │           │   │   │   ├── cli.py
    │           │   │   │   ├── dotenv.py
    │           │   │   │   ├── env.py
    │           │   │   │   ├── gcp.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── nested_secrets.py
    │           │   │   │   ├── pyproject.py
    │           │   │   │   ├── secrets.py
    │           │   │   │   ├── toml.py
    │           │   │   │   └── yaml.py
    │           │   │   ├── types.py
    │           │   │   └── utils.py
    │           │   ├── utils.py
    │           │   └── version.py
    │           ├── pydantic_settings-2.16.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── pygments
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── cmdline.py
    │           │   ├── console.py
    │           │   ├── filter.py
    │           │   ├── filters
    │           │   │   └── __init__.py
    │           │   ├── formatter.py
    │           │   ├── formatters
    │           │   │   ├── __init__.py
    │           │   │   ├── _mapping.py
    │           │   │   ├── bbcode.py
    │           │   │   ├── groff.py
    │           │   │   ├── html.py
    │           │   │   ├── img.py
    │           │   │   ├── irc.py
    │           │   │   ├── latex.py
    │           │   │   ├── other.py
    │           │   │   ├── pangomarkup.py
    │           │   │   ├── rtf.py
    │           │   │   ├── svg.py
    │           │   │   ├── terminal.py
    │           │   │   └── terminal256.py
    │           │   ├── lexer.py
    │           │   ├── lexers
    │           │   │   ├── __init__.py
    │           │   │   ├── _ada_builtins.py
    │           │   │   ├── _asy_builtins.py
    │           │   │   ├── _cl_builtins.py
    │           │   │   ├── _cocoa_builtins.py
    │           │   │   ├── _csound_builtins.py
    │           │   │   ├── _css_builtins.py
    │           │   │   ├── _googlesql_builtins.py
    │           │   │   ├── _julia_builtins.py
    │           │   │   ├── _lasso_builtins.py
    │           │   │   ├── _lilypond_builtins.py
    │           │   │   ├── _lua_builtins.py
    │           │   │   ├── _luau_builtins.py
    │           │   │   ├── _mapping.py
    │           │   │   ├── _mql_builtins.py
    │           │   │   ├── _mysql_builtins.py
    │           │   │   ├── _openedge_builtins.py
    │           │   │   ├── _php_builtins.py
    │           │   │   ├── _postgres_builtins.py
    │           │   │   ├── _qlik_builtins.py
    │           │   │   ├── _scheme_builtins.py
    │           │   │   ├── _scilab_builtins.py
    │           │   │   ├── _sourcemod_builtins.py
    │           │   │   ├── _sql_builtins.py
    │           │   │   ├── _stan_builtins.py
    │           │   │   ├── _stata_builtins.py
    │           │   │   ├── _tsql_builtins.py
    │           │   │   ├── _usd_builtins.py
    │           │   │   ├── _vbscript_builtins.py
    │           │   │   ├── _vim_builtins.py
    │           │   │   ├── actionscript.py
    │           │   │   ├── ada.py
    │           │   │   ├── agile.py
    │           │   │   ├── algebra.py
    │           │   │   ├── ambient.py
    │           │   │   ├── amdgpu.py
    │           │   │   ├── ampl.py
    │           │   │   ├── apdlexer.py
    │           │   │   ├── apl.py
    │           │   │   ├── archetype.py
    │           │   │   ├── arrow.py
    │           │   │   ├── arturo.py
    │           │   │   ├── asc.py
    │           │   │   ├── asm.py
    │           │   │   ├── asn1.py
    │           │   │   ├── automation.py
    │           │   │   ├── bare.py
    │           │   │   ├── basic.py
    │           │   │   ├── bdd.py
    │           │   │   ├── berry.py
    │           │   │   ├── bibtex.py
    │           │   │   ├── bitbake.py
    │           │   │   ├── blueprint.py
    │           │   │   ├── boa.py
    │           │   │   ├── bqn.py
    │           │   │   ├── business.py
    │           │   │   ├── c_cpp.py
    │           │   │   ├── c_like.py
    │           │   │   ├── capnproto.py
    │           │   │   ├── carbon.py
    │           │   │   ├── cddl.py
    │           │   │   ├── cel.py
    │           │   │   ├── chapel.py
    │           │   │   ├── clean.py
    │           │   │   ├── codeql.py
    │           │   │   ├── comal.py
    │           │   │   ├── compiled.py
    │           │   │   ├── configs.py
    │           │   │   ├── console.py
    │           │   │   ├── cplint.py
    │           │   │   ├── crystal.py
    │           │   │   ├── csound.py
    │           │   │   ├── css.py
    │           │   │   ├── d.py
    │           │   │   ├── dalvik.py
    │           │   │   ├── data.py
    │           │   │   ├── dax.py
    │           │   │   ├── devicetree.py
    │           │   │   ├── diff.py
    │           │   │   ├── dns.py
    │           │   │   ├── dotnet.py
    │           │   │   ├── dsls.py
    │           │   │   ├── dylan.py
    │           │   │   ├── ecl.py
    │           │   │   ├── eiffel.py
    │           │   │   ├── elm.py
    │           │   │   ├── elpi.py
    │           │   │   ├── email.py
    │           │   │   ├── erlang.py
    │           │   │   ├── esoteric.py
    │           │   │   ├── ezhil.py
    │           │   │   ├── factor.py
    │           │   │   ├── fantom.py
    │           │   │   ├── felix.py
    │           │   │   ├── fift.py
    │           │   │   ├── floscript.py
    │           │   │   ├── forth.py
    │           │   │   ├── fortran.py
    │           │   │   ├── foxpro.py
    │           │   │   ├── freefem.py
    │           │   │   ├── func.py
    │           │   │   ├── functional.py
    │           │   │   ├── futhark.py
    │           │   │   ├── gcodelexer.py
    │           │   │   ├── gdscript.py
    │           │   │   ├── gleam.py
    │           │   │   ├── go.py
    │           │   │   ├── grammar_notation.py
    │           │   │   ├── graph.py
    │           │   │   ├── graphics.py
    │           │   │   ├── graphql.py
    │           │   │   ├── graphviz.py
    │           │   │   ├── gsql.py
    │           │   │   ├── hare.py
    │           │   │   ├── haskell.py
    │           │   │   ├── haxe.py
    │           │   │   ├── hdl.py
    │           │   │   ├── hexdump.py
    │           │   │   ├── html.py
    │           │   │   ├── idl.py
    │           │   │   ├── igor.py
    │           │   │   ├── inferno.py
    │           │   │   ├── installers.py
    │           │   │   ├── int_fiction.py
    │           │   │   ├── iolang.py
    │           │   │   ├── j.py
    │           │   │   ├── javascript.py
    │           │   │   ├── jmespath.py
    │           │   │   ├── jslt.py
    │           │   │   ├── json5.py
    │           │   │   ├── jsonnet.py
    │           │   │   ├── jsx.py
    │           │   │   ├── julia.py
    │           │   │   ├── jvm.py
    │           │   │   ├── kuin.py
    │           │   │   ├── kusto.py
    │           │   │   ├── ldap.py
    │           │   │   ├── lean.py
    │           │   │   ├── lilypond.py
    │           │   │   ├── lisp.py
    │           │   │   ├── macaulay2.py
    │           │   │   ├── make.py
    │           │   │   ├── maple.py
    │           │   │   ├── markup.py
    │           │   │   ├── math.py
    │           │   │   ├── matlab.py
    │           │   │   ├── maxima.py
    │           │   │   ├── meson.py
    │           │   │   ├── mime.py
    │           │   │   ├── minecraft.py
    │           │   │   ├── mips.py
    │           │   │   ├── ml.py
    │           │   │   ├── modeling.py
    │           │   │   ├── modula2.py
    │           │   │   ├── mojo.py
    │           │   │   ├── monte.py
    │           │   │   ├── mosel.py
    │           │   │   ├── ncl.py
    │           │   │   ├── nimrod.py
    │           │   │   ├── nit.py
    │           │   │   ├── nix.py
    │           │   │   ├── numbair.py
    │           │   │   ├── oberon.py
    │           │   │   ├── objective.py
    │           │   │   ├── ooc.py
    │           │   │   ├── openscad.py
    │           │   │   ├── other.py
    │           │   │   ├── parasail.py
    │           │   │   ├── parsers.py
    │           │   │   ├── pascal.py
    │           │   │   ├── pawn.py
    │           │   │   ├── pddl.py
    │           │   │   ├── perl.py
    │           │   │   ├── phix.py
    │           │   │   ├── php.py
    │           │   │   ├── pointless.py
    │           │   │   ├── pony.py
    │           │   │   ├── praat.py
    │           │   │   ├── procfile.py
    │           │   │   ├── prolog.py
    │           │   │   ├── promql.py
    │           │   │   ├── prql.py
    │           │   │   ├── ptx.py
    │           │   │   ├── purescript.py
    │           │   │   ├── python.py
    │           │   │   ├── q.py
    │           │   │   ├── qlik.py
    │           │   │   ├── qvt.py
    │           │   │   ├── r.py
    │           │   │   ├── rdf.py
    │           │   │   ├── rebol.py
    │           │   │   ├── rego.py
    │           │   │   ├── rell.py
    │           │   │   ├── resource.py
    │           │   │   ├── ride.py
    │           │   │   ├── rita.py
    │           │   │   ├── rnc.py
    │           │   │   ├── roboconf.py
    │           │   │   ├── robotframework.py
    │           │   │   ├── ruby.py
    │           │   │   ├── rust.py
    │           │   │   ├── sas.py
    │           │   │   ├── savi.py
    │           │   │   ├── scdoc.py
    │           │   │   ├── scripting.py
    │           │   │   ├── sgf.py
    │           │   │   ├── shell.py
    │           │   │   ├── sieve.py
    │           │   │   ├── slash.py
    │           │   │   ├── smalltalk.py
    │           │   │   ├── smithy.py
    │           │   │   ├── smv.py
    │           │   │   ├── snobol.py
    │           │   │   ├── solidity.py
    │           │   │   ├── soong.py
    │           │   │   ├── sophia.py
    │           │   │   ├── special.py
    │           │   │   ├── spice.py
    │           │   │   ├── sql.py
    │           │   │   ├── srcinfo.py
    │           │   │   ├── stata.py
    │           │   │   ├── supercollider.py
    │           │   │   ├── tablegen.py
    │           │   │   ├── tact.py
    │           │   │   ├── tal.py
    │           │   │   ├── tcl.py
    │           │   │   ├── teal.py
    │           │   │   ├── templates.py
    │           │   │   ├── teraterm.py
    │           │   │   ├── testing.py
    │           │   │   ├── text.py
    │           │   │   ├── textedit.py
    │           │   │   ├── textfmts.py
    │           │   │   ├── theorem.py
    │           │   │   ├── thingsdb.py
    │           │   │   ├── tlb.py
    │           │   │   ├── tls.py
    │           │   │   ├── tnt.py
    │           │   │   ├── trafficscript.py
    │           │   │   ├── typoscript.py
    │           │   │   ├── typst.py
    │           │   │   ├── ul4.py
    │           │   │   ├── unicon.py
    │           │   │   ├── urbi.py
    │           │   │   ├── usd.py
    │           │   │   ├── varnish.py
    │           │   │   ├── verification.py
    │           │   │   ├── verifpal.py
    │           │   │   ├── vip.py
    │           │   │   ├── vyper.py
    │           │   │   ├── web.py
    │           │   │   ├── webassembly.py
    │           │   │   ├── webidl.py
    │           │   │   ├── webmisc.py
    │           │   │   ├── wgsl.py
    │           │   │   ├── whiley.py
    │           │   │   ├── wowtoc.py
    │           │   │   ├── wren.py
    │           │   │   ├── x10.py
    │           │   │   ├── xorg.py
    │           │   │   ├── yang.py
    │           │   │   ├── yara.py
    │           │   │   └── zig.py
    │           │   ├── modeline.py
    │           │   ├── plugin.py
    │           │   ├── regexopt.py
    │           │   ├── scanner.py
    │           │   ├── sphinxext.py
    │           │   ├── style.py
    │           │   ├── styles
    │           │   │   ├── __init__.py
    │           │   │   ├── _mapping.py
    │           │   │   ├── abap.py
    │           │   │   ├── algol.py
    │           │   │   ├── algol_nu.py
    │           │   │   ├── arduino.py
    │           │   │   ├── autumn.py
    │           │   │   ├── borland.py
    │           │   │   ├── bw.py
    │           │   │   ├── coffee.py
    │           │   │   ├── colorful.py
    │           │   │   ├── default.py
    │           │   │   ├── dracula.py
    │           │   │   ├── emacs.py
    │           │   │   ├── friendly.py
    │           │   │   ├── friendly_grayscale.py
    │           │   │   ├── fruity.py
    │           │   │   ├── gh_dark.py
    │           │   │   ├── gruvbox.py
    │           │   │   ├── igor.py
    │           │   │   ├── inkpot.py
    │           │   │   ├── lightbulb.py
    │           │   │   ├── lilypond.py
    │           │   │   ├── lovelace.py
    │           │   │   ├── manni.py
    │           │   │   ├── material.py
    │           │   │   ├── monokai.py
    │           │   │   ├── murphy.py
    │           │   │   ├── native.py
    │           │   │   ├── night_owl.py
    │           │   │   ├── nord.py
    │           │   │   ├── onedark.py
    │           │   │   ├── paraiso_dark.py
    │           │   │   ├── paraiso_light.py
    │           │   │   ├── pastie.py
    │           │   │   ├── perldoc.py
    │           │   │   ├── rainbow_dash.py
    │           │   │   ├── rrt.py
    │           │   │   ├── sas.py
    │           │   │   ├── solarized.py
    │           │   │   ├── staroffice.py
    │           │   │   ├── stata_dark.py
    │           │   │   ├── stata_light.py
    │           │   │   ├── tango.py
    │           │   │   ├── trac.py
    │           │   │   ├── vim.py
    │           │   │   ├── vs.py
    │           │   │   ├── xcode.py
    │           │   │   └── zenburn.py
    │           │   ├── token.py
    │           │   ├── unistring.py
    │           │   └── util.py
    │           ├── pygments-2.21.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       ├── AUTHORS
    │           │       └── LICENSE
    │           ├── pymupdf
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _apply_pages.py
    │           │   ├── _build.py
    │           │   ├── _extra.so
    │           │   ├── _features.so
    │           │   ├── _mupdf.so
    │           │   ├── _table_headers.py
    │           │   ├── _table_refine.py
    │           │   ├── _table_spans.py
    │           │   ├── _table_union.py
    │           │   ├── _tgif.so
    │           │   ├── _wxcolors.py
    │           │   ├── extra.py
    │           │   ├── features.py
    │           │   ├── layout
    │           │   │   ├── DocumentLayoutAnalyzer.py
    │           │   │   ├── MultiProcessWrapper.py
    │           │   │   ├── __init__.py
    │           │   │   ├── _build.py
    │           │   │   ├── common_util.py
    │           │   │   ├── onnx
    │           │   │   │   ├── BoxRFDGNN.py
    │           │   │   │   ├── DefaultSorter.py
    │           │   │   │   ├── GlobalConfig.py
    │           │   │   │   ├── HTMLGenerator.py
    │           │   │   │   ├── ImageFeatureExtractorV1.py
    │           │   │   │   ├── ImageFeatureExtractorV2.py
    │           │   │   │   ├── LayoutProbAnalyzer.py
    │           │   │   │   ├── MarkdownGenerator.py
    │           │   │   │   ├── MarkdownHTMLTableGenerator.py
    │           │   │   │   ├── TableGridExtractor.py
    │           │   │   │   ├── TableGridExtractorV1A.py
    │           │   │   │   ├── TableGridExtractorV1B.py
    │           │   │   │   ├── TableGridExtractorV2.py
    │           │   │   │   ├── TableGridExtractorV2A.py
    │           │   │   │   ├── TableGridExtractorV2B.py
    │           │   │   │   ├── TableGridExtractorV3.py
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── common_util.py
    │           │   │   │   ├── global_config.yaml
    │           │   │   │   └── table_grid_types.py
    │           │   │   ├── presidio
    │           │   │   │   ├── feature_computation.py
    │           │   │   │   └── graph.py
    │           │   │   ├── pymupdf_util.py
    │           │   │   ├── pymupdf_util_base.py
    │           │   │   ├── pymupdf_util_edge.py
    │           │   │   ├── pymupdf_util_ext.py
    │           │   │   ├── pymupdf_util_imf.py
    │           │   │   ├── pymupdf_util_jf.py
    │           │   │   ├── pymupdf_util_rf.py
    │           │   │   ├── pymupdf_util_yf.py
    │           │   │   ├── resources
    │           │   │   │   └── onnx
    │           │   │   │       ├── feature_imf1.onnx
    │           │   │   │       ├── feature_imf2.onnx
    │           │   │   │       ├── layout_imf1.onnx
    │           │   │   │       ├── layout_imf1.yaml
    │           │   │   │       ├── layout_rf2.4.1+imf1.onnx
    │           │   │   │       ├── layout_rf2.4.1+imf1.yaml
    │           │   │   │       ├── layout_rf2.4.1.onnx
    │           │   │   │       ├── layout_rf2.4.1.yaml
    │           │   │   │       ├── table_grid_model_v1.onnx
    │           │   │   │       ├── table_grid_model_v1_old.onnx
    │           │   │   │       ├── table_grid_model_v1a.onnx
    │           │   │   │       ├── table_grid_model_v1t.onnx
    │           │   │   │       ├── table_grid_model_v2_conn.onnx
    │           │   │   │       ├── table_grid_model_v2_grid.onnx
    │           │   │   │       ├── table_grid_model_v2c.onnx
    │           │   │   │       ├── table_grid_model_v3.onnx
    │           │   │   │       ├── table_grid_model_v4.onnx
    │           │   │   │       ├── table_grid_model_v4_do.onnx
    │           │   │   │       └── table_grid_model_v4_ep.onnx
    │           │   │   └── roi_pooling.py
    │           │   ├── libmupdf.so.28.6
    │           │   ├── libmupdfcpp.so.28.6
    │           │   ├── mupdf-devel
    │           │   │   ├── include
    │           │   │   │   └── mupdf
    │           │   │   │       ├── classes.h
    │           │   │   │       ├── classes2.h
    │           │   │   │       ├── exceptions.h
    │           │   │   │       ├── extra.h
    │           │   │   │       ├── fitz
    │           │   │   │       │   ├── archive.h
    │           │   │   │       │   ├── band-writer.h
    │           │   │   │       │   ├── barcode.h
    │           │   │   │       │   ├── bidi.h
    │           │   │   │       │   ├── bitmap.h
    │           │   │   │       │   ├── buffer.h
    │           │   │   │       │   ├── color.h
    │           │   │   │       │   ├── compress.h
    │           │   │   │       │   ├── compressed-buffer.h
    │           │   │   │       │   ├── config.h
    │           │   │   │       │   ├── context.h
    │           │   │   │       │   ├── crypt.h
    │           │   │   │       │   ├── deskew.h
    │           │   │   │       │   ├── device.h
    │           │   │   │       │   ├── display-list.h
    │           │   │   │       │   ├── document.h
    │           │   │   │       │   ├── export.h
    │           │   │   │       │   ├── filter.h
    │           │   │   │       │   ├── font.h
    │           │   │   │       │   ├── geometry.h
    │           │   │   │       │   ├── getopt.h
    │           │   │   │       │   ├── glyph-cache.h
    │           │   │   │       │   ├── glyph.h
    │           │   │   │       │   ├── hash.h
    │           │   │   │       │   ├── heap-imp.h
    │           │   │   │       │   ├── heap.h
    │           │   │   │       │   ├── hyphen.h
    │           │   │   │       │   ├── image.h
    │           │   │   │       │   ├── json.h
    │           │   │   │       │   ├── link.h
    │           │   │   │       │   ├── log.h
    │           │   │   │       │   ├── options.h
    │           │   │   │       │   ├── outline.h
    │           │   │   │       │   ├── output-svg.h
    │           │   │   │       │   ├── output.h
    │           │   │   │       │   ├── path.h
    │           │   │   │       │   ├── pixmap.h
    │           │   │   │       │   ├── pool.h
    │           │   │   │       │   ├── regexp.h
    │           │   │   │       │   ├── separation.h
    │           │   │   │       │   ├── shade.h
    │           │   │   │       │   ├── store.h
    │           │   │   │       │   ├── story-writer.h
    │           │   │   │       │   ├── story.h
    │           │   │   │       │   ├── stream.h
    │           │   │   │       │   ├── string-util.h
    │           │   │   │       │   ├── structured-text.h
    │           │   │   │       │   ├── system.h
    │           │   │   │       │   ├── text.h
    │           │   │   │       │   ├── track-usage.h
    │           │   │   │       │   ├── transition.h
    │           │   │   │       │   ├── tree.h
    │           │   │   │       │   ├── types.h
    │           │   │   │       │   ├── util.h
    │           │   │   │       │   ├── version.h
    │           │   │   │       │   ├── write-pixmap.h
    │           │   │   │       │   ├── writer.h
    │           │   │   │       │   └── xml.h
    │           │   │   │       ├── fitz.h
    │           │   │   │       ├── functions.h
    │           │   │   │       ├── helpers
    │           │   │   │       │   ├── mu-office-lib.h
    │           │   │   │       │   ├── mu-threads.h
    │           │   │   │       │   └── pkcs7-openssl.h
    │           │   │   │       ├── html.h
    │           │   │   │       ├── internal.h
    │           │   │   │       ├── memento.h
    │           │   │   │       ├── pdf
    │           │   │   │       │   ├── annot.h
    │           │   │   │       │   ├── clean.h
    │           │   │   │       │   ├── cmap.h
    │           │   │   │       │   ├── crypt.h
    │           │   │   │       │   ├── document.h
    │           │   │   │       │   ├── event.h
    │           │   │   │       │   ├── font.h
    │           │   │   │       │   ├── form.h
    │           │   │   │       │   ├── image-rewriter.h
    │           │   │   │       │   ├── interpret.h
    │           │   │   │       │   ├── javascript.h
    │           │   │   │       │   ├── name-table.h
    │           │   │   │       │   ├── object.h
    │           │   │   │       │   ├── page.h
    │           │   │   │       │   ├── parse.h
    │           │   │   │       │   ├── recolor.h
    │           │   │   │       │   ├── resource.h
    │           │   │   │       │   ├── xref.h
    │           │   │   │       │   └── zugferd.h
    │           │   │   │       ├── pdf.h
    │           │   │   │       └── ucdn.h
    │           │   │   └── lib
    │           │   │       └── libmupdf-threads.a
    │           │   ├── mupdf.py
    │           │   ├── mupdf_info.py
    │           │   ├── py.typed
    │           │   ├── pymupdf.py
    │           │   ├── show_features.py
    │           │   ├── table.py
    │           │   ├── tgif.py
    │           │   └── utils.py
    │           ├── pymupdf-2.1.dist-info
    │           │   ├── COPYING
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── README.md
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── entry_points.txt
    │           ├── pymupdf4llm
    │           │   ├── __init__.py
    │           │   ├── _build.py
    │           │   ├── batch_converter.py
    │           │   ├── helpers
    │           │   │   ├── chunking
    │           │   │   │   ├── README.md
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── boundary_scorer.py
    │           │   │   │   ├── chunk_assembler.py
    │           │   │   │   ├── chunked_document.py
    │           │   │   │   ├── models.py
    │           │   │   │   ├── sentence_builder.py
    │           │   │   │   ├── serializer.py
    │           │   │   │   ├── text_source.py
    │           │   │   │   └── token_utils.py
    │           │   │   ├── document_layout.py
    │           │   │   ├── get_text_lines.py
    │           │   │   ├── multi_column.py
    │           │   │   ├── progress.py
    │           │   │   ├── pymupdf_rag.py
    │           │   │   ├── table_html
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── core.py
    │           │   │   │   └── reconstruct.py
    │           │   │   └── utils.py
    │           │   ├── llama
    │           │   │   └── pdf_markdown_reader.py
    │           │   ├── ocr
    │           │   │   ├── __init__.py
    │           │   │   ├── analyze_page.py
    │           │   │   ├── compute_ocr_features.py
    │           │   │   ├── detect_rapidocr.py
    │           │   │   ├── exec_ocr_interface.py
    │           │   │   ├── get_culled_pixmap.py
    │           │   │   ├── ocr_decision_model.onnx
    │           │   │   ├── paddleocr_api.py
    │           │   │   ├── paddletess_api.py
    │           │   │   ├── rapidocr_391_backend.py
    │           │   │   ├── rapidocr_api.py
    │           │   │   ├── rapidocr_onnx_backend.py
    │           │   │   ├── rapidtess_api.py
    │           │   │   └── tesseract_api.py
    │           │   ├── versions_file.py
    │           │   └── worker_sizing.py
    │           ├── pymupdf4llm-2.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   └── WHEEL
    │           ├── pymupdf_layout-2.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   └── WHEEL
    │           ├── pytesseract
    │           │   ├── __init__.py
    │           │   └── pytesseract.py
    │           ├── pytesseract-0.3.13.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── top_level.txt
    │           ├── pytest
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   └── py.typed
    │           ├── pytest-9.2.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── pytest_asyncio
    │           │   ├── __init__.py
    │           │   ├── plugin.py
    │           │   └── py.typed
    │           ├── pytest_asyncio-1.5.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── python_dateutil-2.9.0.post0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── top_level.txt
    │           │   └── zip-safe
    │           ├── python_dotenv-1.2.4.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── python_magic-0.4.27.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── python_multipart
    │           │   ├── __init__.py
    │           │   ├── decoders.py
    │           │   ├── exceptions.py
    │           │   ├── multipart.py
    │           │   └── py.typed
    │           ├── python_multipart-0.0.33.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE.txt
    │           ├── pyyaml-6.0.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── redis
    │           │   ├── __init__.py
    │           │   ├── _defaults.py
    │           │   ├── _himport_exec.py
    │           │   ├── _parsers
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── commands.py
    │           │   │   ├── encoders.py
    │           │   │   ├── helpers.py
    │           │   │   ├── hiredis.py
    │           │   │   ├── resp2.py
    │           │   │   ├── resp3.py
    │           │   │   ├── response_callbacks.py
    │           │   │   └── socket.py
    │           │   ├── asyncio
    │           │   │   ├── __init__.py
    │           │   │   ├── _himport_exec.py
    │           │   │   ├── client.py
    │           │   │   ├── cluster.py
    │           │   │   ├── connection.py
    │           │   │   ├── http
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── http_client.py
    │           │   │   ├── keyspace_notifications.py
    │           │   │   ├── lock.py
    │           │   │   ├── maint_notifications.py
    │           │   │   ├── multidb
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── client.py
    │           │   │   │   ├── command_executor.py
    │           │   │   │   ├── config.py
    │           │   │   │   ├── database.py
    │           │   │   │   ├── event.py
    │           │   │   │   ├── failover.py
    │           │   │   │   ├── failure_detector.py
    │           │   │   │   └── healthcheck.py
    │           │   │   ├── observability
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── recorder.py
    │           │   │   ├── retry.py
    │           │   │   ├── sentinel.py
    │           │   │   └── utils.py
    │           │   ├── auth
    │           │   │   ├── __init__.py
    │           │   │   ├── err.py
    │           │   │   ├── idp.py
    │           │   │   ├── token.py
    │           │   │   └── token_manager.py
    │           │   ├── background.py
    │           │   ├── backoff.py
    │           │   ├── cache.py
    │           │   ├── client.py
    │           │   ├── cluster.py
    │           │   ├── commands
    │           │   │   ├── __init__.py
    │           │   │   ├── bf
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── commands.py
    │           │   │   │   └── info.py
    │           │   │   ├── cluster.py
    │           │   │   ├── core.py
    │           │   │   ├── helpers.py
    │           │   │   ├── json
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _util.py
    │           │   │   │   ├── commands.py
    │           │   │   │   ├── decoders.py
    │           │   │   │   └── path.py
    │           │   │   ├── policies.py
    │           │   │   ├── redismodules.py
    │           │   │   ├── search
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _util.py
    │           │   │   │   ├── aggregation.py
    │           │   │   │   ├── commands.py
    │           │   │   │   ├── dialect.py
    │           │   │   │   ├── document.py
    │           │   │   │   ├── field.py
    │           │   │   │   ├── hybrid_query.py
    │           │   │   │   ├── hybrid_result.py
    │           │   │   │   ├── index_definition.py
    │           │   │   │   ├── profile_information.py
    │           │   │   │   ├── query.py
    │           │   │   │   ├── querystring.py
    │           │   │   │   ├── reducers.py
    │           │   │   │   ├── result.py
    │           │   │   │   └── suggestion.py
    │           │   │   ├── sentinel.py
    │           │   │   ├── timeseries
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── commands.py
    │           │   │   │   ├── info.py
    │           │   │   │   └── utils.py
    │           │   │   └── vectorset
    │           │   │       ├── __init__.py
    │           │   │       ├── commands.py
    │           │   │       └── utils.py
    │           │   ├── connection.py
    │           │   ├── crc.py
    │           │   ├── credentials.py
    │           │   ├── data_structure.py
    │           │   ├── driver_info.py
    │           │   ├── event.py
    │           │   ├── exceptions.py
    │           │   ├── himport.py
    │           │   ├── http
    │           │   │   ├── __init__.py
    │           │   │   └── http_client.py
    │           │   ├── keyspace_notifications.py
    │           │   ├── lock.py
    │           │   ├── maint_notifications.py
    │           │   ├── multidb
    │           │   │   ├── __init__.py
    │           │   │   ├── circuit.py
    │           │   │   ├── client.py
    │           │   │   ├── command_executor.py
    │           │   │   ├── config.py
    │           │   │   ├── database.py
    │           │   │   ├── event.py
    │           │   │   ├── exception.py
    │           │   │   ├── failover.py
    │           │   │   └── failure_detector.py
    │           │   ├── observability
    │           │   │   ├── __init__.py
    │           │   │   ├── attributes.py
    │           │   │   ├── config.py
    │           │   │   ├── metrics.py
    │           │   │   ├── providers.py
    │           │   │   ├── recorder.py
    │           │   │   └── registry.py
    │           │   ├── ocsp.py
    │           │   ├── py.typed
    │           │   ├── retry.py
    │           │   ├── sentinel.py
    │           │   ├── typing.py
    │           │   └── utils.py
    │           ├── redis-8.1.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── requests
    │           │   ├── __init__.py
    │           │   ├── __version__.py
    │           │   ├── _internal_utils.py
    │           │   ├── _types.py
    │           │   ├── adapters.py
    │           │   ├── api.py
    │           │   ├── auth.py
    │           │   ├── certs.py
    │           │   ├── compat.py
    │           │   ├── cookies.py
    │           │   ├── exceptions.py
    │           │   ├── help.py
    │           │   ├── hooks.py
    │           │   ├── models.py
    │           │   ├── packages.py
    │           │   ├── py.typed
    │           │   ├── sessions.py
    │           │   ├── status_codes.py
    │           │   ├── structures.py
    │           │   └── utils.py
    │           ├── requests-2.34.2.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── LICENSE
    │           │   │   └── NOTICE
    │           │   └── top_level.txt
    │           ├── six-1.17.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── six.py
    │           ├── sniffio
    │           │   ├── __init__.py
    │           │   ├── _impl.py
    │           │   ├── _tests
    │           │   │   ├── __init__.py
    │           │   │   └── test_sniffio.py
    │           │   ├── _version.py
    │           │   └── py.typed
    │           ├── sniffio-1.3.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── LICENSE.APACHE2
    │           │   ├── LICENSE.MIT
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── sqlalchemy
    │           │   ├── __init__.py
    │           │   ├── connectors
    │           │   │   ├── __init__.py
    │           │   │   ├── aioodbc.py
    │           │   │   ├── asyncio.py
    │           │   │   └── pyodbc.py
    │           │   ├── dialects
    │           │   │   ├── __init__.py
    │           │   │   ├── _typing.py
    │           │   │   ├── mssql
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── aioodbc.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── information_schema.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── mssqlpython.py
    │           │   │   │   ├── provision.py
    │           │   │   │   ├── pymssql.py
    │           │   │   │   └── pyodbc.py
    │           │   │   ├── mysql
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _mariadb_shim.py
    │           │   │   │   ├── aiomysql.py
    │           │   │   │   ├── asyncmy.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── cymysql.py
    │           │   │   │   ├── dml.py
    │           │   │   │   ├── enumerated.py
    │           │   │   │   ├── expression.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── mariadb.py
    │           │   │   │   ├── mariadbconnector.py
    │           │   │   │   ├── mysqlconnector.py
    │           │   │   │   ├── mysqldb.py
    │           │   │   │   ├── provision.py
    │           │   │   │   ├── pymysql.py
    │           │   │   │   ├── pyodbc.py
    │           │   │   │   ├── reflection.py
    │           │   │   │   ├── reserved_words.py
    │           │   │   │   └── types.py
    │           │   │   ├── oracle
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── cx_oracle.py
    │           │   │   │   ├── dictionary.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── oracledb.py
    │           │   │   │   ├── provision.py
    │           │   │   │   ├── types.py
    │           │   │   │   └── vector.py
    │           │   │   ├── postgresql
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── _psycopg_common.py
    │           │   │   │   ├── array.py
    │           │   │   │   ├── asyncpg.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── bitstring.py
    │           │   │   │   ├── dml.py
    │           │   │   │   ├── ext.py
    │           │   │   │   ├── hstore.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── named_types.py
    │           │   │   │   ├── operators.py
    │           │   │   │   ├── pg8000.py
    │           │   │   │   ├── pg_catalog.py
    │           │   │   │   ├── provision.py
    │           │   │   │   ├── psycopg.py
    │           │   │   │   ├── psycopg2.py
    │           │   │   │   ├── psycopg2cffi.py
    │           │   │   │   ├── ranges.py
    │           │   │   │   └── types.py
    │           │   │   ├── sqlite
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── aiosqlite.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── dml.py
    │           │   │   │   ├── json.py
    │           │   │   │   ├── provision.py
    │           │   │   │   ├── pysqlcipher.py
    │           │   │   │   └── pysqlite.py
    │           │   │   └── type_migration_guidelines.txt
    │           │   ├── engine
    │           │   │   ├── __init__.py
    │           │   │   ├── _processors_cy.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _processors_cy.py
    │           │   │   ├── _result_cy.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _result_cy.py
    │           │   │   ├── _row_cy.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _row_cy.py
    │           │   │   ├── _util_cy.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _util_cy.py
    │           │   │   ├── base.py
    │           │   │   ├── characteristics.py
    │           │   │   ├── create.py
    │           │   │   ├── cursor.py
    │           │   │   ├── default.py
    │           │   │   ├── events.py
    │           │   │   ├── interfaces.py
    │           │   │   ├── mock.py
    │           │   │   ├── processors.py
    │           │   │   ├── reflection.py
    │           │   │   ├── result.py
    │           │   │   ├── row.py
    │           │   │   ├── strategies.py
    │           │   │   ├── url.py
    │           │   │   └── util.py
    │           │   ├── event
    │           │   │   ├── __init__.py
    │           │   │   ├── api.py
    │           │   │   ├── attr.py
    │           │   │   ├── base.py
    │           │   │   ├── legacy.py
    │           │   │   └── registry.py
    │           │   ├── events.py
    │           │   ├── exc.py
    │           │   ├── ext
    │           │   │   ├── __init__.py
    │           │   │   ├── associationproxy.py
    │           │   │   ├── asyncio
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── engine.py
    │           │   │   │   ├── exc.py
    │           │   │   │   ├── result.py
    │           │   │   │   ├── scoping.py
    │           │   │   │   └── session.py
    │           │   │   ├── automap.py
    │           │   │   ├── baked.py
    │           │   │   ├── compiler.py
    │           │   │   ├── declarative
    │           │   │   │   ├── __init__.py
    │           │   │   │   └── extensions.py
    │           │   │   ├── horizontal_shard.py
    │           │   │   ├── hybrid.py
    │           │   │   ├── indexable.py
    │           │   │   ├── instrumentation.py
    │           │   │   ├── mutable.py
    │           │   │   ├── orderinglist.py
    │           │   │   └── serializer.py
    │           │   ├── future
    │           │   │   ├── __init__.py
    │           │   │   └── engine.py
    │           │   ├── inspection.py
    │           │   ├── log.py
    │           │   ├── orm
    │           │   │   ├── __init__.py
    │           │   │   ├── _orm_constructors.py
    │           │   │   ├── _typing.py
    │           │   │   ├── attributes.py
    │           │   │   ├── base.py
    │           │   │   ├── bulk_persistence.py
    │           │   │   ├── clsregistry.py
    │           │   │   ├── collections.py
    │           │   │   ├── context.py
    │           │   │   ├── decl_api.py
    │           │   │   ├── decl_base.py
    │           │   │   ├── dependency.py
    │           │   │   ├── descriptor_props.py
    │           │   │   ├── dynamic.py
    │           │   │   ├── evaluator.py
    │           │   │   ├── events.py
    │           │   │   ├── exc.py
    │           │   │   ├── identity.py
    │           │   │   ├── instrumentation.py
    │           │   │   ├── interfaces.py
    │           │   │   ├── loading.py
    │           │   │   ├── mapped_collection.py
    │           │   │   ├── mapper.py
    │           │   │   ├── path_registry.py
    │           │   │   ├── persistence.py
    │           │   │   ├── properties.py
    │           │   │   ├── query.py
    │           │   │   ├── relationships.py
    │           │   │   ├── scoping.py
    │           │   │   ├── session.py
    │           │   │   ├── state.py
    │           │   │   ├── state_changes.py
    │           │   │   ├── strategies.py
    │           │   │   ├── strategy_options.py
    │           │   │   ├── sync.py
    │           │   │   ├── unitofwork.py
    │           │   │   ├── util.py
    │           │   │   └── writeonly.py
    │           │   ├── pool
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   ├── events.py
    │           │   │   └── impl.py
    │           │   ├── py.typed
    │           │   ├── schema.py
    │           │   ├── sql
    │           │   │   ├── __init__.py
    │           │   │   ├── _annotated_cols.py
    │           │   │   ├── _cache_key_cy.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _cache_key_cy.py
    │           │   │   ├── _dml_constructors.py
    │           │   │   ├── _elements_constructors.py
    │           │   │   ├── _orm_types.py
    │           │   │   ├── _selectable_constructors.py
    │           │   │   ├── _typing.py
    │           │   │   ├── _util_cy.cpython-314-x86_64-linux-gnu.so
    │           │   │   ├── _util_cy.pxd
    │           │   │   ├── _util_cy.py
    │           │   │   ├── annotation.py
    │           │   │   ├── base.py
    │           │   │   ├── cache_key.py
    │           │   │   ├── coercions.py
    │           │   │   ├── compiler.py
    │           │   │   ├── crud.py
    │           │   │   ├── ddl.py
    │           │   │   ├── default_comparator.py
    │           │   │   ├── dml.py
    │           │   │   ├── elements.py
    │           │   │   ├── events.py
    │           │   │   ├── expression.py
    │           │   │   ├── functions.py
    │           │   │   ├── lambdas.py
    │           │   │   ├── naming.py
    │           │   │   ├── operators.py
    │           │   │   ├── roles.py
    │           │   │   ├── schema.py
    │           │   │   ├── selectable.py
    │           │   │   ├── sqltypes.py
    │           │   │   ├── traversals.py
    │           │   │   ├── type_api.py
    │           │   │   ├── util.py
    │           │   │   └── visitors.py
    │           │   ├── testing
    │           │   │   ├── __init__.py
    │           │   │   ├── assertions.py
    │           │   │   ├── assertsql.py
    │           │   │   ├── asyncio.py
    │           │   │   ├── cancellation.py
    │           │   │   ├── config.py
    │           │   │   ├── engines.py
    │           │   │   ├── entities.py
    │           │   │   ├── exclusions.py
    │           │   │   ├── fixtures
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── base.py
    │           │   │   │   ├── mypy.py
    │           │   │   │   ├── orm.py
    │           │   │   │   └── sql.py
    │           │   │   ├── pickleable.py
    │           │   │   ├── plugin
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── bootstrap.py
    │           │   │   │   ├── plugin_base.py
    │           │   │   │   └── pytestplugin.py
    │           │   │   ├── profiles_file.py
    │           │   │   ├── profiling.py
    │           │   │   ├── provision.py
    │           │   │   ├── requirements.py
    │           │   │   ├── schema.py
    │           │   │   ├── suite
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── test_cte.py
    │           │   │   │   ├── test_ddl.py
    │           │   │   │   ├── test_dialect.py
    │           │   │   │   ├── test_insert.py
    │           │   │   │   ├── test_reflection.py
    │           │   │   │   ├── test_results.py
    │           │   │   │   ├── test_rowcount.py
    │           │   │   │   ├── test_select.py
    │           │   │   │   ├── test_sequence.py
    │           │   │   │   ├── test_table_via_select.py
    │           │   │   │   ├── test_types.py
    │           │   │   │   ├── test_unicode_ddl.py
    │           │   │   │   └── test_update_delete.py
    │           │   │   ├── util.py
    │           │   │   └── warnings.py
    │           │   ├── types.py
    │           │   └── util
    │           │       ├── __init__.py
    │           │       ├── _collections.py
    │           │       ├── _collections_cy.cpython-314-x86_64-linux-gnu.so
    │           │       ├── _collections_cy.pxd
    │           │       ├── _collections_cy.py
    │           │       ├── _has_cython.py
    │           │       ├── _immutabledict_cy.cpython-314-x86_64-linux-gnu.so
    │           │       ├── _immutabledict_cy.py
    │           │       ├── compat.py
    │           │       ├── concurrency.py
    │           │       ├── cython.py
    │           │       ├── deprecations.py
    │           │       ├── langhelpers.py
    │           │       ├── preloaded.py
    │           │       ├── queue.py
    │           │       ├── tool_support.py
    │           │       ├── topological.py
    │           │       └── typing.py
    │           ├── sqlalchemy-2.1.8.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── AUTHORS
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── starlette
    │           │   ├── __init__.py
    │           │   ├── _exception_handler.py
    │           │   ├── _utils.py
    │           │   ├── applications.py
    │           │   ├── authentication.py
    │           │   ├── background.py
    │           │   ├── concurrency.py
    │           │   ├── config.py
    │           │   ├── convertors.py
    │           │   ├── datastructures.py
    │           │   ├── endpoints.py
    │           │   ├── exceptions.py
    │           │   ├── formparsers.py
    │           │   ├── middleware
    │           │   │   ├── __init__.py
    │           │   │   ├── authentication.py
    │           │   │   ├── base.py
    │           │   │   ├── body_limit.py
    │           │   │   ├── cors.py
    │           │   │   ├── errors.py
    │           │   │   ├── exceptions.py
    │           │   │   ├── gzip.py
    │           │   │   ├── httpsredirect.py
    │           │   │   ├── opentelemetry.py
    │           │   │   ├── sessions.py
    │           │   │   ├── trustedhost.py
    │           │   │   └── wsgi.py
    │           │   ├── py.typed
    │           │   ├── requests.py
    │           │   ├── responses.py
    │           │   ├── routing.py
    │           │   ├── schemas.py
    │           │   ├── staticfiles.py
    │           │   ├── status.py
    │           │   ├── templating.py
    │           │   ├── testclient.py
    │           │   ├── types.py
    │           │   └── websockets.py
    │           ├── starlette-1.10.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── tabulate
    │           │   └── __init__.py
    │           ├── tabulate-0.10.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── tokenizers
    │           │   ├── __init__.py
    │           │   ├── __init__.pyi
    │           │   ├── decoders
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── implementations
    │           │   │   ├── __init__.py
    │           │   │   ├── base_tokenizer.py
    │           │   │   ├── bert_wordpiece.py
    │           │   │   ├── byte_level_bpe.py
    │           │   │   ├── char_level_bpe.py
    │           │   │   ├── sentencepiece_bpe.py
    │           │   │   └── sentencepiece_unigram.py
    │           │   ├── models
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── normalizers
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── pre_tokenizers
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── processors
    │           │   │   ├── __init__.py
    │           │   │   └── __init__.pyi
    │           │   ├── py.typed
    │           │   ├── tokenizers.abi3.so
    │           │   ├── tokenizers.pyi
    │           │   ├── tools
    │           │   │   ├── __init__.py
    │           │   │   ├── visualizer-styles.css
    │           │   │   └── visualizer.py
    │           │   └── trainers
    │           │       ├── __init__.py
    │           │       └── __init__.pyi
    │           ├── tokenizers-0.23.3.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── sboms
    │           │       └── tokenizers-python.cyclonedx.json
    │           ├── tqdm
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _main.py
    │           │   ├── _monitor.py
    │           │   ├── _tqdm.py
    │           │   ├── _tqdm_gui.py
    │           │   ├── _tqdm_notebook.py
    │           │   ├── _tqdm_pandas.py
    │           │   ├── _utils.py
    │           │   ├── asyncio.py
    │           │   ├── auto.py
    │           │   ├── autonotebook.py
    │           │   ├── cli.py
    │           │   ├── completion.sh
    │           │   ├── contrib
    │           │   │   ├── __init__.py
    │           │   │   ├── bells.py
    │           │   │   ├── concurrent.py
    │           │   │   ├── discord.py
    │           │   │   ├── itertools.py
    │           │   │   ├── logging.py
    │           │   │   ├── slack.py
    │           │   │   ├── telegram.py
    │           │   │   └── utils_worker.py
    │           │   ├── dask.py
    │           │   ├── gui.py
    │           │   ├── keras.py
    │           │   ├── notebook.py
    │           │   ├── rich.py
    │           │   ├── std.py
    │           │   ├── tk.py
    │           │   ├── tqdm.1
    │           │   ├── utils.py
    │           │   └── version.py
    │           ├── tqdm-4.70.1.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENCE
    │           │   └── top_level.txt
    │           ├── truststore
    │           │   ├── __init__.py
    │           │   ├── _api.py
    │           │   ├── _macos.py
    │           │   ├── _openssl.py
    │           │   ├── _ssl_constants.py
    │           │   ├── _windows.py
    │           │   └── py.typed
    │           ├── truststore-0.10.5.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── typing_extensions-4.16.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── typing_extensions.py
    │           ├── typing_inspection
    │           │   ├── __init__.py
    │           │   ├── introspection.py
    │           │   ├── py.typed
    │           │   ├── typing_objects.py
    │           │   └── typing_objects.pyi
    │           ├── typing_inspection-0.4.5.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE
    │           ├── tzlocal
    │           │   ├── __init__.py
    │           │   ├── py.typed
    │           │   ├── unix.py
    │           │   ├── utils.py
    │           │   ├── win32.py
    │           │   └── windows_tz.py
    │           ├── tzlocal-5.4.5.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE.txt
    │           │   └── top_level.txt
    │           ├── urllib3
    │           │   ├── __init__.py
    │           │   ├── _base_connection.py
    │           │   ├── _collections.py
    │           │   ├── _request_methods.py
    │           │   ├── _version.py
    │           │   ├── connection.py
    │           │   ├── connectionpool.py
    │           │   ├── contrib
    │           │   │   ├── __init__.py
    │           │   │   ├── emscripten
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── connection.py
    │           │   │   │   ├── emscripten_fetch_worker.js
    │           │   │   │   ├── fetch.py
    │           │   │   │   ├── request.py
    │           │   │   │   └── response.py
    │           │   │   ├── pyopenssl.py
    │           │   │   └── socks.py
    │           │   ├── exceptions.py
    │           │   ├── fields.py
    │           │   ├── filepost.py
    │           │   ├── http2
    │           │   │   ├── __init__.py
    │           │   │   ├── connection.py
    │           │   │   └── probe.py
    │           │   ├── poolmanager.py
    │           │   ├── py.typed
    │           │   ├── response.py
    │           │   └── util
    │           │       ├── __init__.py
    │           │       ├── connection.py
    │           │       ├── proxy.py
    │           │       ├── request.py
    │           │       ├── response.py
    │           │       ├── retry.py
    │           │       ├── ssl_.py
    │           │       ├── ssl_match_hostname.py
    │           │       ├── ssltransport.py
    │           │       ├── timeout.py
    │           │       ├── url.py
    │           │       ├── util.py
    │           │       └── wait.py
    │           ├── urllib3-2.8.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── licenses
    │           │       └── LICENSE.txt
    │           ├── uvicorn
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _ansi.py
    │           │   ├── _compat.py
    │           │   ├── _subprocess.py
    │           │   ├── _types.py
    │           │   ├── config.py
    │           │   ├── importer.py
    │           │   ├── lifespan
    │           │   │   ├── __init__.py
    │           │   │   ├── off.py
    │           │   │   └── on.py
    │           │   ├── logging.py
    │           │   ├── loops
    │           │   │   ├── __init__.py
    │           │   │   ├── asyncio.py
    │           │   │   ├── auto.py
    │           │   │   ├── uvloop.py
    │           │   │   └── zuvloop.py
    │           │   ├── main.py
    │           │   ├── middleware
    │           │   │   ├── __init__.py
    │           │   │   ├── asgi2.py
    │           │   │   ├── message_logger.py
    │           │   │   ├── proxy_headers.py
    │           │   │   └── wsgi.py
    │           │   ├── protocols
    │           │   │   ├── __init__.py
    │           │   │   ├── http
    │           │   │   │   ├── __init__.py
    │           │   │   │   ├── auto.py
    │           │   │   │   ├── auto_zttp_impl.py
    │           │   │   │   ├── flow_control.py
    │           │   │   │   ├── h11_impl.py
    │           │   │   │   ├── httptools_impl.py
    │           │   │   │   ├── zttp_h2_impl.py
    │           │   │   │   └── zttp_impl.py
    │           │   │   ├── utils.py
    │           │   │   └── websockets
    │           │   │       ├── __init__.py
    │           │   │       ├── auto.py
    │           │   │       ├── websockets_impl.py
    │           │   │       ├── websockets_sansio_impl.py
    │           │   │       └── wsproto_impl.py
    │           │   ├── py.typed
    │           │   ├── server.py
    │           │   ├── supervisors
    │           │   │   ├── __init__.py
    │           │   │   ├── basereload.py
    │           │   │   ├── multiprocess.py
    │           │   │   ├── statreload.py
    │           │   │   └── watchfilesreload.py
    │           │   └── workers.py
    │           ├── uvicorn-0.54.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── REQUESTED
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   └── licenses
    │           │       └── LICENSE.md
    │           ├── uvloop
    │           │   ├── __init__.py
    │           │   ├── _noop.py
    │           │   ├── _testbase.py
    │           │   ├── _version.py
    │           │   ├── cbhandles.pxd
    │           │   ├── cbhandles.pyx
    │           │   ├── dns.pyx
    │           │   ├── errors.pyx
    │           │   ├── handles
    │           │   │   ├── async_.pxd
    │           │   │   ├── async_.pyx
    │           │   │   ├── basetransport.pxd
    │           │   │   ├── basetransport.pyx
    │           │   │   ├── check.pxd
    │           │   │   ├── check.pyx
    │           │   │   ├── fsevent.pxd
    │           │   │   ├── fsevent.pyx
    │           │   │   ├── handle.pxd
    │           │   │   ├── handle.pyx
    │           │   │   ├── idle.pxd
    │           │   │   ├── idle.pyx
    │           │   │   ├── pipe.pxd
    │           │   │   ├── pipe.pyx
    │           │   │   ├── poll.pxd
    │           │   │   ├── poll.pyx
    │           │   │   ├── process.pxd
    │           │   │   ├── process.pyx
    │           │   │   ├── stream.pxd
    │           │   │   ├── stream.pyx
    │           │   │   ├── streamserver.pxd
    │           │   │   ├── streamserver.pyx
    │           │   │   ├── tcp.pxd
    │           │   │   ├── tcp.pyx
    │           │   │   ├── timer.pxd
    │           │   │   ├── timer.pyx
    │           │   │   ├── udp.pxd
    │           │   │   └── udp.pyx
    │           │   ├── includes
    │           │   │   ├── __init__.py
    │           │   │   ├── consts.pxi
    │           │   │   ├── debug.pxd
    │           │   │   ├── flowcontrol.pxd
    │           │   │   ├── python.pxd
    │           │   │   ├── stdlib.pxi
    │           │   │   ├── system.pxd
    │           │   │   └── uv.pxd
    │           │   ├── loop.cpython-314-x86_64-linux-gnu.so
    │           │   ├── loop.pxd
    │           │   ├── loop.pyi
    │           │   ├── loop.pyx
    │           │   ├── lru.pyx
    │           │   ├── pseudosock.pyx
    │           │   ├── py.typed
    │           │   ├── request.pxd
    │           │   ├── request.pyx
    │           │   ├── server.pxd
    │           │   ├── server.pyx
    │           │   ├── sslproto.pxd
    │           │   └── sslproto.pyx
    │           ├── uvloop-0.23.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   ├── LICENSE-APACHE
    │           │   │   └── LICENSE-MIT
    │           │   └── top_level.txt
    │           ├── vine
    │           │   ├── __init__.py
    │           │   ├── abstract.py
    │           │   ├── funtools.py
    │           │   ├── promises.py
    │           │   ├── synchronization.py
    │           │   └── utils.py
    │           ├── vine-5.1.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── LICENSE
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   └── top_level.txt
    │           ├── watchfiles
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── _rust_notify.abi3.so
    │           │   ├── _rust_notify.pyi
    │           │   ├── cli.py
    │           │   ├── filters.py
    │           │   ├── main.py
    │           │   ├── py.typed
    │           │   ├── run.py
    │           │   └── version.py
    │           ├── watchfiles-1.3.0.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── sboms
    │           │       └── watchfiles_rust_notify.cyclonedx.json
    │           ├── wcwidth
    │           │   ├── __init__.py
    │           │   ├── _clip.py
    │           │   ├── _constants.py
    │           │   ├── _wcswidth.py
    │           │   ├── _wcwidth.py
    │           │   ├── _wcwidth_c.abi3.so
    │           │   ├── _wcwidth_c.pyi
    │           │   ├── _width.py
    │           │   ├── align.py
    │           │   ├── bisearch.py
    │           │   ├── control_codes.py
    │           │   ├── escape_sequences.py
    │           │   ├── grapheme.py
    │           │   ├── hyperlink.py
    │           │   ├── py.typed
    │           │   ├── sgr_state.py
    │           │   ├── table_ambiguous.py
    │           │   ├── table_grapheme.py
    │           │   ├── table_grapheme_overrides
    │           │   │   ├── __init__.py
    │           │   │   ├── _known_058c7585.py
    │           │   │   ├── _known_2148ff29.py
    │           │   │   ├── _known_244dc88b.py
    │           │   │   ├── _known_336a71a1.py
    │           │   │   ├── _known_33ac73f2.py
    │           │   │   ├── _known_3a1895d5.py
    │           │   │   ├── _known_59180a0d.py
    │           │   │   ├── _known_65c6beb5.py
    │           │   │   ├── _known_78f828e8.py
    │           │   │   ├── _known_8c2ae14d.py
    │           │   │   ├── _known_900356bf.py
    │           │   │   ├── _known_97904ece.py
    │           │   │   ├── _known_a5880eeb.py
    │           │   │   ├── _known_b6d33cf4.py
    │           │   │   ├── _known_c57c295b.py
    │           │   │   ├── _known_cf02297d.py
    │           │   │   ├── _known_e18ac6a7.py
    │           │   │   ├── _known_e2b75ee3.py
    │           │   │   ├── _known_fb5fd79b.py
    │           │   │   ├── _known_fdc99132.py
    │           │   │   └── _registry.py
    │           │   ├── table_mc.py
    │           │   ├── table_overrides.py
    │           │   ├── table_term_programs.py
    │           │   ├── table_vs15.py
    │           │   ├── table_vs16.py
    │           │   ├── table_wide.py
    │           │   ├── table_zero.py
    │           │   ├── text_sizing.py
    │           │   ├── textwrap.py
    │           │   ├── unicode_versions.py
    │           │   └── wcwidth.py
    │           ├── wcwidth-0.9.4.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           ├── websockets
    │           │   ├── __init__.py
    │           │   ├── __main__.py
    │           │   ├── asyncio
    │           │   │   ├── __init__.py
    │           │   │   ├── client.py
    │           │   │   ├── connection.py
    │           │   │   ├── messages.py
    │           │   │   ├── router.py
    │           │   │   └── server.py
    │           │   ├── auth.py
    │           │   ├── cli.py
    │           │   ├── client.py
    │           │   ├── connection.py
    │           │   ├── datastructures.py
    │           │   ├── exceptions.py
    │           │   ├── extensions
    │           │   │   ├── __init__.py
    │           │   │   ├── base.py
    │           │   │   └── permessage_deflate.py
    │           │   ├── frames.py
    │           │   ├── headers.py
    │           │   ├── http11.py
    │           │   ├── imports.py
    │           │   ├── legacy
    │           │   │   ├── __init__.py
    │           │   │   ├── auth.py
    │           │   │   ├── client.py
    │           │   │   ├── exceptions.py
    │           │   │   ├── framing.py
    │           │   │   ├── handshake.py
    │           │   │   ├── http.py
    │           │   │   ├── protocol.py
    │           │   │   └── server.py
    │           │   ├── protocol.py
    │           │   ├── proxy.py
    │           │   ├── py.typed
    │           │   ├── server.py
    │           │   ├── speedups.c
    │           │   ├── speedups.cpython-314-x86_64-linux-gnu.so
    │           │   ├── speedups.pyi
    │           │   ├── streams.py
    │           │   ├── sync
    │           │   │   ├── __init__.py
    │           │   │   ├── client.py
    │           │   │   ├── connection.py
    │           │   │   ├── messages.py
    │           │   │   ├── router.py
    │           │   │   ├── server.py
    │           │   │   └── utils.py
    │           │   ├── trio
    │           │   │   ├── __init__.py
    │           │   │   ├── client.py
    │           │   │   ├── connection.py
    │           │   │   ├── messages.py
    │           │   │   ├── router.py
    │           │   │   ├── server.py
    │           │   │   └── utils.py
    │           │   ├── typing.py
    │           │   ├── uri.py
    │           │   ├── utils.py
    │           │   └── version.py
    │           ├── websockets-17.4.dist-info
    │           │   ├── INSTALLER
    │           │   ├── METADATA
    │           │   ├── RECORD
    │           │   ├── WHEEL
    │           │   ├── entry_points.txt
    │           │   ├── licenses
    │           │   │   └── LICENSE
    │           │   └── top_level.txt
    │           └── yaml
    │               ├── __init__.py
    │               ├── _yaml.cpython-314-x86_64-linux-gnu.so
    │               ├── composer.py
    │               ├── constructor.py
    │               ├── cyaml.py
    │               ├── dumper.py
    │               ├── emitter.py
    │               ├── error.py
    │               ├── events.py
    │               ├── loader.py
    │               ├── nodes.py
    │               ├── parser.py
    │               ├── reader.py
    │               ├── representer.py
    │               ├── resolver.py
    │               ├── scanner.py
    │               ├── serializer.py
    │               └── tokens.py
    ├── lib64 -> lib
    └── pyvenv.cfg

1217 directories, 10778 files
```
