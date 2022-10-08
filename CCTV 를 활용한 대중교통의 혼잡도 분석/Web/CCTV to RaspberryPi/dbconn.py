import pymysql
# 사용할 DB의 정보
db = pymysql.connect(host='',
                                    user='',
                                    password='',
                                    db='',
                                    charset='',
                                    read_timeout=2,
                                    write_timeout=2,
                                    connect_timeout=2
                                    )

