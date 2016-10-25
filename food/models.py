# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Addfooddesc(models.Model):
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code')
    seq_num = models.SmallIntegerField()
    start_date = models.DateTimeField(db_column='start_ date', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    end_date = models.DateTimeField(blank=True, null=True)
    additional_food_description = models.CharField(db_column='Additional food description', max_length=80, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        
        db_table = 'addfooddesc'
        unique_together = (('food_code', 'seq_num'),)


class Allergens(models.Model):
    species = models.CharField(max_length=255, blank=True, null=True)
    common = models.CharField(max_length=255, blank=True, null=True)
    allergen = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    allergen_group = models.CharField(max_length=255, blank=True, null=True)
    gi = models.BigIntegerField(blank=True, null=True)
    uniprot_accession = models.CharField(max_length=1156, blank=True, null=True)
    database = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        
        db_table = 'allergens'


class Countries(models.Model):
    country_name = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'countries'


class DashDiet(models.Model):
    id = models.IntegerField(primary_key=True)
    meal = models.ForeignKey('DashFooddesc', models.DO_NOTHING, db_column='meal', blank=True, null=True)
    servings = models.FloatField()
    grains = models.FloatField(blank=True, null=True)
    vegetables = models.FloatField(blank=True, null=True)
    fruits = models.FloatField(blank=True, null=True)
    milk_products = models.FloatField(blank=True, null=True)
    meats_fish_poultry = models.FloatField(blank=True, null=True)
    nuts_seeds_legumes = models.FloatField(blank=True, null=True)
    fats_oils = models.FloatField(blank=True, null=True)
    sweets_added_sugars = models.FloatField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'dash_diet'


class DashFooddesc(models.Model):
    id = models.IntegerField(primary_key=True)
    meal = models.CharField(max_length=45)

    class Meta:
        
        db_table = 'dash_fooddesc'


class Dashfnddslinks(models.Model):
    id = models.IntegerField(primary_key=True)
    dash_meal = models.IntegerField()
    ingredient = models.CharField(max_length=45, blank=True, null=True)
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code')
    measure_name = models.CharField(max_length=45, blank=True, null=True)
    measures_amount = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'dashfnddslinks'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        
        db_table = 'django_migrations'


class Dri(models.Model):
    nutrient = models.CharField(max_length=255, blank=True, null=True)
    nutrient_code = models.ForeignKey('Nutdesc', models.DO_NOTHING, db_column='nutrient_code')
    country = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    min_age = models.FloatField(blank=True, null=True)
    max_age = models.FloatField(blank=True, null=True)
    pregn_lact = models.CharField(max_length=255, blank=True, null=True)
    min_intake = models.FloatField(blank=True, null=True)
    max_intake = models.FloatField(blank=True, null=True)
    units = models.CharField(max_length=255, blank=True, null=True)
    rec_type = models.CharField(max_length=255, blank=True, null=True)
    sd = models.FloatField(blank=True, null=True)
    add_amount = models.FloatField(blank=True, null=True)
    cond = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    src_author = models.CharField(max_length=255, blank=True, null=True)
    src_title = models.CharField(max_length=255, blank=True, null=True)
    year = models.BigIntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'dri'



        

class Fnddsnutval(models.Model):
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code')
    nutrient_code = models.ForeignKey('Nutdesc', models.DO_NOTHING, db_column='nutrient_code')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    nutrient_value = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'fnddsnutval'
        unique_together = (('food_code', 'nutrient_code', 'start_date'),)


class Fnddsreccount(models.Model):
    full_file_name = models.CharField(max_length=50)
    no_of_records = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'fnddsreccount'


class Fnddssrlinks(models.Model):
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code')
    start_date = models.DateTimeField(db_column='start _date')  # Field renamed to remove unsuitable characters.
    end_date = models.DateTimeField()
    seq_num = models.SmallIntegerField()
    sr_code = models.IntegerField(blank=True, null=True)
    sr_description = models.CharField(max_length=240, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    measure = models.CharField(max_length=3, blank=True, null=True)
    portion_code = models.IntegerField(blank=True, null=True)
    retention_code = models.SmallIntegerField(blank=True, null=True)
    flag = models.SmallIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    change_type_to_sr_code = models.CharField(max_length=1, blank=True, null=True)
    change_type_to_weight = models.CharField(max_length=1, blank=True, null=True)
    change_type_to_retn_code = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        
        db_table = 'fnddssrlinks'
        unique_together = (('food_code', 'start_date', 'end_date', 'seq_num'),)


class Foodallergens(models.Model):
    food = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food', related_name='allergens')
    ingredient = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='ingredient')
    allergen = models.ForeignKey(Allergens, models.DO_NOTHING, db_column='allergen')

    class Meta:
        
        db_table = 'foodallergens'


class Foodportiondesc(models.Model):
    portion_code = models.ForeignKey('Foodweights', models.DO_NOTHING, db_column='portion_code')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    portion_description = models.CharField(max_length=120, blank=True, null=True)
    change_type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        
        db_table = 'foodportiondesc'
        unique_together = (('portion_code', 'start_date'),)


class Foodsubcodelinks(models.Model):
    food_code = models.ForeignKey('Foodweights', models.DO_NOTHING, db_column='food_code', related_name='subcodelink')
    subcode = models.ForeignKey('Foodweights', models.DO_NOTHING, db_column='subcode')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'foodsubcodelinks'
        unique_together = (('food_code', 'subcode'),)


class Foodweights(models.Model):
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code', blank=True, null=True)
    subcode = models.IntegerField(blank=True, null=True)
    seq_num = models.SmallIntegerField(blank=True, null=True)
    portion_code = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    portion_weight = models.FloatField(blank=True, null=True)
    change_type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        
        db_table = 'foodweights'
        unique_together = (('food_code', 'subcode', 'seq_num', 'portion_code', 'start_date'),)


class Fped(models.Model):
    id = models.IntegerField(primary_key=True)
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code', blank=True, null=True)
    mod_code = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    f_citmlb = models.FloatField(blank=True, null=True)
    f_other = models.FloatField(blank=True, null=True)
    f_juice = models.FloatField(blank=True, null=True)
    f_total = models.FloatField(blank=True, null=True)
    v_drkgr = models.FloatField(blank=True, null=True)
    v_redor_tomato = models.FloatField(blank=True, null=True)
    v_redor_other = models.FloatField(blank=True, null=True)
    v_redor_total = models.FloatField(blank=True, null=True)
    v_starchy_potato = models.FloatField(blank=True, null=True)
    v_starchy_other = models.FloatField(blank=True, null=True)
    v_starchy_total = models.FloatField(blank=True, null=True)
    v_other = models.FloatField(blank=True, null=True)
    v_total = models.FloatField(blank=True, null=True)
    v_legumes = models.FloatField(blank=True, null=True)
    g_whole = models.FloatField(blank=True, null=True)
    g_refined = models.FloatField(blank=True, null=True)
    g_total = models.FloatField(blank=True, null=True)
    pf_meat = models.FloatField(blank=True, null=True)
    pf_curedmeat = models.FloatField(blank=True, null=True)
    pf_organ = models.FloatField(blank=True, null=True)
    pf_poult = models.FloatField(blank=True, null=True)
    pf_seafd_hi = models.FloatField(blank=True, null=True)
    pf_seafd_low = models.FloatField(blank=True, null=True)
    pf_mps_total = models.FloatField(blank=True, null=True)
    pf_eggs = models.FloatField(blank=True, null=True)
    pf_soy = models.FloatField(blank=True, null=True)
    pf_nutsds = models.FloatField(blank=True, null=True)
    pf_legumes = models.FloatField(blank=True, null=True)
    pf_total = models.FloatField(blank=True, null=True)
    d_milk = models.FloatField(blank=True, null=True)
    d_yogurt = models.FloatField(blank=True, null=True)
    d_cheese = models.FloatField(blank=True, null=True)
    d_total = models.FloatField(blank=True, null=True)
    oils = models.FloatField(blank=True, null=True)
    solid_fats = models.FloatField(blank=True, null=True)
    add_sugars = models.FloatField(blank=True, null=True)
    a_drinks = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'fped'


class GeneralRecommendations(models.Model):
    message = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    official = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'general_recommendations'


class GlutenFree(models.Model):
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code')

    class Meta:
        
        db_table = 'gluten_free'


class HeiFoodGroups(models.Model):
    food_group = models.CharField(max_length=255)
    measure_name = models.CharField(max_length=255)
    max_score = models.IntegerField()
    min_score_amount = models.FloatField()
    max_score_amount = models.FloatField()

    class Meta:
        
        db_table = 'hei_food_groups'


class Hied(models.Model):
    food_code = models.ForeignKey('Mainfooddesc', models.DO_NOTHING, db_column='food_code', blank=True, null=True)
    food_group = models.ForeignKey(HeiFoodGroups, models.DO_NOTHING, db_column='food_group', blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'hied'


class Mainfooddesc(models.Model):
    food_code = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    main_food_description = models.CharField(max_length=200, blank=True, null=True)
    fortification_identifier = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'mainfooddesc'


class MealPatternDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal = models.ForeignKey('MealPatternFooddesc', models.DO_NOTHING)
    measure_name = models.CharField(max_length=255)
    measures_amount = models.CharField(max_length=255)
    requirement = models.IntegerField()
    age_group = models.CharField(max_length=255)
    age_from = models.FloatField(blank=True)
    age_to = models.FloatField(blank=True)

    class Meta:
        
        db_table = 'meal_pattern_diet'


class MealPatternGroups(models.Model):
    food_group = models.CharField(max_length=255)
    measure_name = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'meal_pattern_food_groups'


class MealPatternFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'meal_pattern_fooddesc'


        
class Moddesc(models.Model):
    modification_code = models.IntegerField(unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    modification_description = models.TextField(blank=True, null=True)
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code', blank=True, null=True)

    class Meta:
        
        db_table = 'moddesc'


class Modnutval(models.Model):
    modification_code = models.ForeignKey(Moddesc, models.DO_NOTHING, db_column='modification_code')
    nutrient_code = models.ForeignKey('Nutdesc', models.DO_NOTHING, db_column='nutrient_code')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    nutrient_value = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'modnutval'
        unique_together = (('modification_code', 'nutrient_code', 'start_date'),)


class Moistnfatadjust(models.Model):
    food_code = models.ForeignKey(Fnddssrlinks, models.DO_NOTHING, db_column='food_code')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    moisture_change = models.FloatField(blank=True, null=True)
    fat_change = models.FloatField(blank=True, null=True)
    type_of_fat = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'moistnfatadjust'
        unique_together = (('food_code', 'start_date'),)


class Mped(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code', blank=True, null=True)
    food_group = models.ForeignKey('MyplateFoodGroups', models.DO_NOTHING, db_column='food_group', blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'mped'


class MyplateDescription(models.Model):
    food_group = models.ForeignKey('MyplateFoodGroups', models.DO_NOTHING, db_column='food_group', blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    nutrients = models.TextField(blank=True, null=True)

    class Meta:
        
        db_table = 'myplate_description'


class MyplateDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal = models.ForeignKey('MyplateFooddesc', models.DO_NOTHING)
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'myplate_diet'


class MyplateFoodGroups(models.Model):
    food_group = models.CharField(max_length=255)
    measure_name = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'myplate_food_groups'


class MyplateFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'myplate_fooddesc'


class MyplateRecommendations(models.Model):
    min_age = models.FloatField(blank=True, null=True)
    max_age = models.FloatField(blank=True, null=True)
    calories_intake = models.FloatField(blank=True, null=True)
    food_group = models.ForeignKey(MyplateFoodGroups, models.DO_NOTHING, db_column='food_group', blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'myplate_recommendations'


class Myplatefnddslinks(models.Model):
    meal = models.ForeignKey(MyplateFooddesc, models.DO_NOTHING, db_column='meal')
    ingredient = models.CharField(max_length=255)
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()
    servings = models.IntegerField()
    sr_code = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'myplatefnddslinks'


class NutData(models.Model):
    id = models.IntegerField(primary_key=True)
    ndb_no = models.BigIntegerField(blank=True, null=True)
    nutr_no = models.BigIntegerField(blank=True, null=True)
    nutr_val = models.FloatField(blank=True, null=True)
    num_data_pts = models.BigIntegerField(blank=True, null=True)
    std_error = models.FloatField(blank=True, null=True)
    src_cd = models.BigIntegerField(blank=True, null=True)
    deriv_cd = models.CharField(max_length=63, blank=True, null=True)
    ref_ndb_no = models.FloatField(blank=True, null=True)
    add_nutr_mark = models.CharField(max_length=63, blank=True, null=True)
    num_studies = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    df = models.FloatField(blank=True, null=True)
    low_eb = models.FloatField(blank=True, null=True)
    up_eb = models.FloatField(blank=True, null=True)
    stat_cmt = models.CharField(max_length=63, blank=True, null=True)
    addmod_date = models.CharField(max_length=63, blank=True, null=True)
    cc = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'nut_data'


class Nutdesc(models.Model):
    nutrient_code = models.SmallIntegerField(primary_key=True)
    nutrient_description = models.CharField(max_length=45, blank=True, null=True)
    tagname = models.CharField(max_length=15, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)
    decimals = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'nutdesc'


class NutrInfo(models.Model):
    nutrient = models.CharField(max_length=255, blank=True, null=True)
    nutrient_code = models.ForeignKey(Nutdesc, models.DO_NOTHING, db_column='nutrient_code')
    nutrient_role = models.TextField()
    deficiency = models.TextField()
    excess = models.TextField()
    sources = models.TextField()

    class Meta:
        
        db_table = 'nutr_info'


class NutrInteractions(models.Model):
    effected_nutrient = models.ForeignKey(Nutdesc, models.DO_NOTHING, db_column='effected_nutrient', related_name='interactions')
    effect = models.IntegerField()
    effector = models.ForeignKey(Nutdesc, models.DO_NOTHING, db_column='effector')
    source = models.TextField()

    class Meta:
        
        db_table = 'nutr_interactions'


class SrAllergens(models.Model):
    sr_code = models.ForeignKey(Fnddssrlinks, models.DO_NOTHING, db_column='sr_code', blank=True, null=True)
    allergens = models.ForeignKey(Allergens, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        
        db_table = 'sr_allergens'


class Subcodedesc(models.Model):
    subcode = models.ForeignKey(Foodsubcodelinks, models.DO_NOTHING, db_column='subcode')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    subcode_description = models.CharField(max_length=80)

    class Meta:
        
        db_table = 'subcodedesc'
        unique_together = (('subcode', 'start_date'),)



class WeekMealPlanUkDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal = models.ForeignKey('WeekMealPlanUkFooddesc', models.DO_NOTHING)
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'week_meal_plan_uk_diet'


class WeekMealPlanUkFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'week_meal_plan_uk_fooddesc'
        
class WeekMealPlanUkMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(WeekMealPlanUkFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'week_meal_plan_uk_mainfooddesc_links'


class Usda5DayDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal = models.ForeignKey('Usda5DayFooddesc', models.DO_NOTHING)
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'usda_5day_diet'


class Usda5DayFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'usda_5day_fooddesc'
        
class Usda5DayMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(Usda5DayFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'usda_5day_mainfooddesc_links'

class ScandinavianDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal = models.ForeignKey('ScandinavianFooddesc', models.DO_NOTHING)
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'scandinavian_diet'


class ScandinavianFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'scandinavian_fooddesc'
        
class ScandinavianMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(ScandinavianFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'scandinavian_mainfooddesc_links'

class Whatscooking(models.Model):
    meal = models.ForeignKey('WhatscookingFooddesc', models.DO_NOTHING, db_column='meal')
    ingredient = models.CharField(max_length=255)
    food_code = models.IntegerField()
    measure_name = models.CharField(max_length=255)
    measure_code = models.IntegerField(blank=True, null=True)
    measures_amount = models.FloatField()
    servings = models.IntegerField()
    sr_code = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'whatscooking'


class WhatscookingFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'whatscooking_fooddesc'
        
class ElementarySchoolDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('ElementarySchoolFooddesc', models.DO_NOTHING)
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'elementary_school_diet'


class ElementarySchoolFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'elementary_school_fooddesc'
        
class ElementarySchoolMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(ElementarySchoolFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'elementary_school_mainfooddesc_links'
        
class MiddleSchoolDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('MiddleSchoolFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'middle_school_diet'


class MiddleSchoolFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'middle_school_fooddesc'
        
class MiddleSchoolMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(MiddleSchoolFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'high_school_mainfooddesc_links'
        
class HighSchoolDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('HighSchoolFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'high_school_diet'


class HighSchoolFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'high_school_fooddesc'
        
class HighSchoolMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(HighSchoolFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'high_school_mainfooddesc_links'

#pregnancy_1_trimester
class Pregnancy1TrimesterDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('Pregnancy1TrimesterFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'pregnancy_1_trimester_diet'


class Pregnancy1TrimesterFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'pregnancy_1_trimester_fooddesc'
        
class Pregnancy1TrimesterMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(Pregnancy1TrimesterFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'pregnancy_1_trimester_mainfooddesc_links'

#pregnancy_2_trimester
class Pregnancy2TrimesterDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('Pregnancy2TrimesterFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'pregnancy_2_trimester_diet'


class Pregnancy2TrimesterFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'pregnancy_2_trimester_fooddesc'
        
class Pregnancy2TrimesterMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(Pregnancy2TrimesterFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'pregnancy_2_trimester_mainfooddesc_links'

#pregnancy_3_trimester
class Pregnancy3TrimesterDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('Pregnancy3TrimesterFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'pregnancy_3_trimester_diet'


class Pregnancy3TrimesterFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'pregnancy_3_trimester_fooddesc'
        
class Pregnancy3TrimesterMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(Pregnancy3TrimesterFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'pregnancy_3_trimester_mainfooddesc_links'
#5Aday
class a5AdayDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('a5AdayFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = '5Aday_diet'


class a5AdayFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = '5Aday_fooddesc'
        
class a5AdayMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(a5AdayFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = '5Aday_mainfooddesc_links'

#dash_clinic
class DashClinicDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('DashClinicFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'dash_clinic_diet'


class DashClinicFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'dash_clinic_fooddesc'
        
class DashClinicMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(DashClinicFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'dash_clinic_mainfooddesc_links'
        

class MediterreneanDiet(models.Model):
    meal_id = models.ForeignKey('MediterreneanFooddesc', models.DO_NOTHING, db_column='meal_id')
    time = models.CharField(max_length=255, blank=True, null=True)
    measure_name = models.CharField(max_length=255, blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    measures_amount = models.FloatField(blank=True, null=True)

    class Meta:
        
        db_table = 'mediterrenean_diet'

class MediterreneanFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'mediterrenean_fooddesc'
        
class MediterreneanMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(MediterreneanFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'mediterrenean_mainfooddesc_links'
        unique_together = (('food_code', 'meal'),)


#dash_clinic
class UsdaChildren5DayDiet(models.Model):
    day = models.IntegerField()
    time = models.CharField(max_length=255)
    meal_id = models.ForeignKey('UsdaChildren5DayFooddesc', models.DO_NOTHING, db_column='meal_id')
    measure_name = models.CharField(max_length=255)
    measures_amount = models.FloatField()

    class Meta:
        
        db_table = 'usda_children_5day_diet'


class UsdaChildren5DayFooddesc(models.Model):
    meal = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'usda_children_5day_fooddesc'
        
class UsdaChildren5DayMainfooddesc(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    meal = models.ForeignKey(UsdaChildren5DayFooddesc, models.DO_NOTHING, db_column='meal')

    class Meta:
        
        db_table = 'usda_children_5day_mainfooddesc_links'

class MainFoodDescAllergens(models.Model):
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    allergen = models.ForeignKey(Allergens, models.DO_NOTHING, db_column='allergen_id')
    ingredient = models.CharField(max_length=255,  db_column='ingredient')
    
    class Meta:
        
        db_table = 'mainfooddesc_allergens_links'

class PregAvoidFood(models.Model):
    food = models.CharField(max_length=255, db_column='food')
    recomend = models.CharField(max_length=255, db_column='recommendation')
    source = models.CharField(max_length=255, db_column='source')
    food_code = models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    
    class Meta:
        
        db_table = 'pregnancy_avoid_food' 
    
    
class a5AdayRecipe(models.Model):
    meal = models.CharField(max_length=255)
    ingredient = models.CharField(max_length=255)
    measure_unit = models.CharField(max_length=255)
    measure_amount = models.FloatField()
    serving = models.IntegerField()
    food_code = models.IntegerField()#models.ForeignKey(Mainfooddesc, models.DO_NOTHING, db_column='food_code')
    sr_code = models.IntegerField()
    
    class Meta:
        
        db_table = '5Aday_recipes'
        
    
    
    
    
    
    
    