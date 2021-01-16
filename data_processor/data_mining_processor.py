import statsmodels.api as sm


def linearregression(dataset, independents, dependent):
    # define the data
    X = dataset[independents]
    y = dataset[dependent]

    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)  # make the predictions by the model

    # Print out the statistics
    return model.summary()


def run(dataset, algo_config,  algorithm_name):
    if algorithm_name.lower().replace(" ", "") == 'linearregression':
        return linearregression(dataset, algo_config["independents"], algo_config["dependent"])

