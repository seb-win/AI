import pandas as pd
import adept, anthropic, character, cohere, glean, huggingface, inflection, jasper, lightricks, openai_script, replit, runway, stability

def main():
    adept_daily = adept.main()
    # anthropic_daily = anthropic.main()
    # character_daily = character.main()
    # cohere_daily = cohere.main()
    # glean_daily = glean.main()
    # huggingface_daily = huggingface.main()
    # inflection_daily = inflection.main()
    # jasper_daily = jasper.main()
    # lightricks_daily = lightricks.main()
    # openai_daily = openai_script.main()
    # replit_daily = replit.main()
    # runway_daily = runway.main()
    # stability_daily = stability.main()
    
    df = pd.DataFrame(columns=['Company', 'Job Count'])
    df.loc[0] = [adept_daily['company'], adept_daily['jobCount']]
    print(df)



if __name__ == "__main__":
    main()