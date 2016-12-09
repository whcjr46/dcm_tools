bq load --source_format=CSV --field_delimiter='\t' --skip_leading_rows=1 \
    isb-cgc:test.TCIA_dcm_metadata \
    dcm_metadata.clean.tsv \
    dcm_metadata.tsv.json

 
