from py2neo import Graph
graph = Graph()

def all_sorted():
    query = '''match (n:CarModel)-[:hasCar]->(m:Car)-[:hasScore]->(s:Score)
        match (m)-[:hasReport]->(r:Report)
        return properties(m) as info, properties(s) as score, properties(r) as report
        order by coalesce(score.score, 0) desc
        limit 50
        '''
    results = graph.data(query)
    results = res_process(results)
    return results


def query_ymm(year, make, model, sortby):
    if sortby == "score":
        orderby = "score.score"
    elif sortby == "price":
        orderby = "info.price"
    elif sortby == "rating":
        orderby = "score.rating_score"
    elif sortby == "mileage/year":
        orderby = "score.mileage_year"

    query = '''match (n:CarModel{make: {make}, model: {model}, year: {year}})-[:hasCar]->(m:Car)-[:hasScore]->(s:Score)
    match (m)-[:hasReport]->(r:Report)
    return properties(m) as info, properties(s) as score, properties(r) as report
    order by ''' + (orderby + " asc" if orderby == "info.price" or orderby == "score.mileage_year" else "coalesce(" + orderby + ", 0) desc") + '''
    limit 50
    '''
    results = graph.data(query, make=make, model=model, year=year)
    results = res_process(results)
    return results


def query_price(price, sortby):
    if sortby == "score":
        orderby = "score.score"
    elif sortby == "price":
        orderby = "info.price"
    elif sortby == "rating":
        orderby = "score.rating_score"
    elif sortby == "mileage/year":
        orderby = "score.mileage_year"

    if price == "< $5,000":
        price_query = "m.price < 5000"
    elif price == "$5,000 - $10,000":
        price_query = "m.price >= 5000 and m.price < 10000"
    elif price == "$10,000 - $15,000":
        price_query = "m.price >= 10000 and m.price < 15000"
    elif price == "$15,000 - $20,000":
        price_query = "m.price >= 15000 and m.price < 20000"
    elif price == "$20,000 - $25,000":
        price_query = "m.price >= 20000 and m.price < 25000"
    elif price == "$25,000 - $30,000":
        price_query = "m.price >= 25000 and m.price < 30000"
    elif price == "> $30,000":
        price_query = "m.price >= 30000"
    query = '''match (n:CarModel)-[:hasCar]->(m:Car)-[:hasScore]->(s:Score)
        match (m)-[:hasReport]->(r:Report)
        where ''' + price_query + '''
        return properties(m) as info, properties(s) as score, properties(r) as report
        order by ''' + (orderby + " asc" if orderby == "info.price" or orderby == "score.mileage_year" else "coalesce(" + orderby + ", 0) desc") + '''
        limit 50
        '''
    results = graph.data(query)
    results = res_process(results)
    return results


def res_process(results):
    for result in results:
        if u'price' in result[u'info']:
            result[u'info'][u'price'] = '${:,.2f}'.format(float(result[u'info'][u'price']))
        if u'tmv_dealer' in result[u'info']:
            result[u'info'][u'tmv_dealer'] = '${:,.2f}'.format(float(result[u'info'][u'tmv_dealer']))
        if u'score' in result[u'score']:
            result[u'score'][u'score'] = '%.2f' % float(result[u'score'][u'score'])
        if u'mileage_year' in result[u'score']:
            result[u'score'][u'mileage_year'] = '%.1f' % float(result[u'score'][u'mileage_year'])
        if u'rating_score' in result[u'score']:
            result[u'score'][u'rating_score'] = '%.0f' % (float(result[u'score'][u'rating_score'])*100)
        if u'price_diff_per' in result[u'score']:
            result[u'score'][u'price_diff_per'] = "{:.0%}".format(float(result[u'score'][u'price_diff_per']))
        if u'warranty' in result[u'report']:
            result[u'report'][u'warranty'] = result[u'report'][u'warranty'].split(";")
        if u'recalls_detail' in result[u'report']:
            result[u'report'][u'recalls_detail'] = result[u'report'][u'recalls_detail'].split(";")
    return results