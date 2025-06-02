import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from google.generativeai.types import GenerationConfig
from google.ai.generativelanguage import SafetySetting, HarmCategory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables.")
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    logger.error(f"Failed to configure Google Generative AI: {e}")
    raise RuntimeError(f"Failed to configure Google Generative AI: {e}")

# --- Model Configuration ---
MODEL_NAME = "gemini-2.5-flash-preview-05-20" # Or your preferred model

# System Prompt - THIS WILL BE VERY LONG AS IT CONTAINS THE ENTIRE TRANSCRIPT
# The actual transcript will be inserted by you into this string.
SYSTEM_PROMPT = """
You are "Sona," an expert breastfeeding consultant and maternal health specialist. You provide evidence-based, practical advice to new mothers and families navigating their breastfeeding journey.

**Core Response Guidelines:**

1. **Natural Voice & Tone:**
   - Speak as a warm, knowledgeable healthcare professional
   - Use an empathetic, supportive, and reassuring tone
   - Be conversational yet professional - like talking to a trusted friend
   - Never reference "courses," "modules," "transcripts," or study materials

2. **Response Structure:**
   - Start with a brief, reassuring opening
   - Organize information in clear, logical sections using headings
   - Use bullet points and numbered lists for easy reading
   - End with practical next steps or encouragement

3. **Content Style:**
   - Be specific and actionable - give clear steps mothers can follow
   - Use simple, clear language that any new mother can understand
   - Include practical tips and real-world examples
   - Focus on what mothers need to know and do right now

4. **Formatting:**
   - Use `**bold text**` for key terms and important points
   - Use `*italic text*` for gentle emphasis
   - Structure with clear headings using `##` and `###`
   - Use bullet points (`-`) and numbered lists (`1.`) for clarity
   - Keep paragraphs short and scannable

5. **Professional Approach:**
   - Base all advice on evidence-based practices
   - Be encouraging while being realistic about challenges
   - Always recommend professional help when needed
   - Never make mothers feel guilty about their feeding choices

**IMPORTANT: Language for Response**
- If the user specifies a language, generate the entire response (answer, headings, everything) in that language.
- Supported languages and their codes: English (en), Hindi (hi), Bengali (bn), Marathi (mr), Kannada (kn), Gujarati (gu).
- If no language is specified, default to English.
- When responding in a non-English language, ensure the tone, detail, and structure are equivalent to an English response based on the guidelines.

** NOTE: All answers needs to be under 250 words.** 

**Knowledge Base:**

(...)

Welcome to breastfeeding the first steps.(...) This comprehensive course is designed for parents and for expecting parents to prepare you for your breastfeeding journey. Whether the journey has already started or is expected to start post delivery. We hope this course provides you with new information, guides you, answers your questions and empowers you to go through the journey of breastfeeding or bottle feeding and be there with your baby through their growing years. Hi, my name is Sonal. I am a mother and a professional in the field of infant and pediatric feeding. So I am living it. Treating issues related to breastfeeding and infant and pediatric feeding every day.

(...)

The beauty of this combination is that you will hear information in this course coming all from my heart with all the emotion for my own children and also coming with evidence based background based from my professional experience.

(...)

The goal of this course is to provide you with information with practical advice and guidance to go through your initial months weeks of breastfeeding. I would highly, highly encourage for fathers in the room, in the house to join this course. It is, I would like to emphasize that this course is specifically really beneficial for fathers to go through to take notes because when the baby comes along, the new mama is quite occupied physically, mentally, harmonially, emotionally. So during that time, if fathers are equipped with the knowledge, they can come up and take kind of help, help and take over the situation.

(...)

So breastfeeding, what is breastfeeding?(...) It is nature's one of most wonderful ways of nourishing babies.(...) Isn't it an incredible thing that we as women have the ability to nourish another human being? Literally a new human can be, can exist and survive based through us, getting nutrition through us. This is as miraculous as it can be. But during childbirth, which is beautiful, there's also a little bit of chaos which is going on and it is kind of part and parcel of the journey. Sometimes during that chaos, during those tough moments, we can miss the right moment, the right technique of initiating breastfeeding.

(...)

And when that happens, because of some unnecessary delays or because of the situation, sometimes the babies are put in the direction of formula feeding, which is completely okay. However, what we want with this course, that you are upfront, upfront equipped with information, with knowledge, which you know, that these are the steps I need to take. As a father, I need to tell the hospital or I need to tell my family. As a mother, I need to remind myself. All those components which come together with knowledge for you to know that this is how you would start your breastfeeding journey. What does first hour after birth mean? What is the correct way of latching the baby? And most important, how do you self care for yourself? You know, how do you take care of yourself and kind of demit all the myths and judgment around breastfeeding and then start your journey.

(...)

All of this information in the beginning, if new parents have or parents who've just become parents have their journey in general, emotionally, physically and mentally will be very different. So we really hope this course guides you and empowers you and equips you with the information we wish to give you. Let's get started. Before we go into the course, I would like to say that we would also have a life workshop. We will also conduct a life workshop on latch techniques and bottle feeding techniques. Suppose this course, when the completion of this course happens, you will receive an invite for a live session. Please join. I will be there on the other side. We will go through your questions from the course and we will also go through different kind of latch techniques and bottle techniques so that you are equipped and ready with the information. Let's get started and see you during the course.

(...)

Our entire course is divided into five modules, as you can see on the slide.(...) In the first module, we will discuss birth, the critical period of birth, first hour post delivery and details about breast milk.

(...)

In our second module, we will talk about the mother and the baby and the importance behind establishing their bond.

(...)

In the third module, we will go through steps in terms of where to start, how to latch, what is a good latch and signs of a good latch.(...) In our module four, we will cover basics in positioning, how to latch baby, what are some basic things we should know as new parents and also signs when the latch is incorrect and we might need professional help.

(...)

In the last module, I would like to demyth some breastfeeding myths. All the modules are important. All the modules are something very close to our heart in terms of knowledge which we wish to share, but especially module number five. I really want that we as new, we really want that we all as new parents do not have the burden of any judgment or any myth or any unknown when we're starting our journey. And just because it was unknown, we could not do it right. So we will focus on demything the breastfeeding myths in our module number five. And as a last thing, I would be there present in life session where we will discuss face to face your questions which you have had out of the course. And we will also do a workshop with regards to latching the baby and even bottle feeding. So let's get started.

(...)

As part of Module 1, the critical period of birth, we will cover essential information for new parents, both fathers and mothers, to ensure they are well prepared for the arrival of their baby. It is especially important for fathers to understand what steps to take in order to support the mother and the baby during this time, so we would really encourage fathers to join up.

(...)

Regardless of the method of childbirth, vaginal or caesarean, the mother is likely to be occupied and tired. Therefore, fathers and other caretakers and family play a crucial role in being aware of the necessary actions and information discussed in this module.(...) As mother may not be in the optimal state to remember everything, the fathers and the families can come up with these points and make sure that they are nicely performed.

    

Let's get started with our first module.

(...)

What is the critical period of birth?

(...)

It is the time when baby transitions from mother's womb to the outside world.

(...)

Newborns move from a fluid-filled environment to an air environment, which they need to adjust to. The mother's arms have been the natural habitat for the baby, so upon birth, they instinctively want their mother.

(...)

This is a natural intranation and it is important for us to understand.(...) Similarly, how we would reach out for air if we are in a swimming pool. Imagine that your head is fully submerged in water, even if you are a great swimmer, and you are in the water for some time, for a few seconds or a few minutes, whatever you are comfortable with. Whenever you push yourself out and you come to grass funeral to get air, you would most probably reach out to a surface.

(...)

Whatever surface you reach out to is going to be the surface you want, basically to calm yourself down to get some air in.

(...)

In this world of birth, that surface for the baby is the mother.

(...)

As soon as baby has come out of the water and is going to learn to breathe in air, they will reach out to their mother.

(...)

This is something which we as new parents, as first-time parents or even second-time parents need to keep in mind.

(...)

In cases where there is a separation between mother and the baby, such as the C-section or when the baby requires maybe some medical care, could be that they have been detected with jaundice, they are usually going to be taken away.(...) So, in that separation, we have to make sure, we have to keep in mind that as soon as the baby comes back, as soon as the mother has, you know, slightly recovered from the C-section or from the anesthesia, they both need to immediately be together.(...) How should they be together is something we will discuss in the coming slides.

(...)

Once the baby has born, the first hour has started.(...) So, what is this first hour and what is its significance?

(...)

This is also known as the golden hour.(...) The golden hour is the first hour post-delivery and is a critical period for both the mother and the newborn.

(...)

This initial hour, I really want all of us as new parents and expecting parents to remember this. This initial hour followed by the birth, it stands apart, serving a unique phase separate from the other activities of breastfeeding to come.(...) So, no matter whatever actions we take in the coming breastfeeding hours, weeks, this specific hour, this first hour, it stands separate and it has its own importance.

(...)

I would read a quote to all of you.(...) "All mammals, including babies, have an innate neuro-behavior and there is a unique period in time in which an event can take place and this innate behavior can be fully expressed."

(...)

I will explain what I mean by this with a non-baby and a non-press feeding example.

(...)

Mostly in all the cultures, so I am from India, so in our Asian cultures, around the time of 24, 25, 26, 27 even,(...) mostly families, society, the people around us, even friends,(...) there is a strong inclination where the families would say to their children, to their young children who are 25, 24 years of age to start looking for a partner, to see if they are liking someone, to sometimes the families they start looking for partners themselves for their kids and to basically go in the direction of finding the right partner they would like to spend their life with.

(...)

So, in the time 26, 27, 28, 29, whenever the time is right, there is a support from the society, from the family to get married.

(...)

The reason behind this is not just that something happens to them around this age. The reason behind this is actually the same concept of innate neuro-behavior.

(...)

During this time when we are 25, 26, 27, our behaviors, our hormones, our developments are in the direction of finding love, are in the direction of finding a right partner, are in the direction of attraction.(...) So it is encouraged and it is rightly so encouraged to use that time to be with someone, to enjoy that face, to live that face and that's why in some cultures even marriages are encouraged around this time. The idea is that during this time the behavior of being with a partner, of being in love, of spending that time together is quite innately strong in our body. The hormones are quite strong, the behavior is quite strong and we have this inclination towards it. The same concept, the same ideology can be applied to the first hour.(...) During the first hour, baby's innate behavior, innate neuroreaction is to wanting to come next to their mother.

(...)

So as soon as the mother and the baby are together in the first hour post delivery, these innate neuro-behaviors, they are expressed fully. And what are these innate neuro-behaviors? We will discuss in the coming slide. But I hope you understand that this is the time when they want to be with their mother, so connecting it to the adult's life with their partner, with their love and in this case the first love is the mother, with their mother to be able to express their innate behaviors, what they actually want to do, they can express that in comfort with their mother.(...) So this is one of the most important reasons to keep in mind that first hour is so significant.

(...)

Now that the baby has been born, our little one is in our arms, they have some basic biological needs which we should know.

(...)

Firstly, they require oxygenation to breathe. As I said in the first slide, they've moved from a water-based to an air-based environment so they need to learn how to breathe.(...) Secondly, they need nutrition to grow and develop.

(...)

Third, they need to maintain a warm body temperature as they are now exposed to different environmental conditions. And fourth, they need protection to ensure their safety and well-being.

(...)

It's important to keep these four fundamental needs in mind as we consider how to best meet them.(...) We will cover how the baby can obtain these needs and how we can provide them in the coming slides. However, it's important to keep these fundamental needs in mind because we would basically be fulfilling them with one person and we will discuss them in the following slides.

(...)

As I just mentioned that the babies are moving from a water-based environment to an air environment so they need to learn how to breathe. They have some biological needs and of course they are small, soft and they look vulnerable. We as adults can have this innate feeling of protecting them and also going by the assumption that they don't know much. Which is correct, of course, they're not in terms of fully developed with their brain capacity, we all know that. However, it is not that they don't know anything.(...) So the capabilities of a newborn is very important for every parent to know because we can leverage them, we can catch them. The first thing is that babies can recognize their mother, her smell, her voice, her touch and this is what gives them the most comfort.

(...)

The second is babies have inherent knowledge of suckling and if given a chance can initiate suckling and drinking from breasts themselves. Yes, so you've heard me right. We are not going to just focus on starting breastfeeding themselves. We will go through all the steps. However, it's important for us to remember that they kind of actually know how to do this. They know the suckling part, they know how to sip and they know that action of suck, rhythm and then swallow already. Maybe some of you have also witnessed it in your ultrasounds that you see your babies(...) sucking their thumbs or their fingers.

(...)

They are fragile and new to the environment. So in order to initiate and perform the task and completely leverage the capabilities they have a breastfeeding initiation environment should be calm, should be relaxed and should be quiet. How to achieve this? What to do? Again, the points we are going to cover in the coming slides, but please remember that yes, they have moved from a water to an air environment. They need our support with breathing, with warmth, with nutrition, with protection. However, they have the capabilities of recognizing their sole provider, their prime provider, which is their mother.

(...)

And they also have the capabilities to suck, suckle and rhythmically swallow.

(...)

Mother's body is going to produce breast milk, of course, but it's going to produce the first milk known as the colstrum.

(...)

So this is a specific slide, which I think is very important again for the family and for the fathers, whoever are going to, you know, going to be there supporting the mother, because it could be a situation that the mother is separate from the baby for any reason and is completely okay. The hospital is taking care of the baby. But when the mother is ready with her colstrum and it has come, the letdown has come, which usually happens in the first hour, we want that first milk to be given to the baby.(...) How we give it, how is it done? It of course depends on the situation. It is ideal if the baby can come to the mother and the breastfeeding can start in the first hour. If that cannot happen, then at least we should still speak to the hospital staff and tell them that we would want when the mother is ready, we would want the breast milk, the first milk to be taken out and given to the baby.(...) Why do we want this? The first thing is it is nutrient rich. It is rich in probiotics. It is rich in proteins, in vitamins, minerals.(...) And the second thing is it is highly rich in antibodies and immune factors. It has a high concentration of immunoglobins. These are the antibodies which babies need to fight infection. It is highly beneficial for gut. A newborn's gut is not matured yet. They need support with it and breast milk, especially the first milk gives that. It is laxative in nature, which means that it will help the baby to pass poop, which is going to be the first poop, which is thick, dark and sticky.

(...)

And it is that bonding and comfort moment which the baby is looking for. So ideally we want the first milk, which is known as the colstrom, to be given to the baby in the first hour by bringing the mother and the baby together. How to do it? We are going to cover in the coming slides. If that does not happen even then, please speak with your hospital, speak with your clinic, your nursing unit that the mother is feeling the breast milk come out. The letdown is happening and we would want to give that first milk to the baby because of the benefits we just discussed.

(...)

The benefits which we discussed of colstrom are not just limited to the first milk. These benefits extend into breast milk throughout the breastfeeding journey.(...) Yes, there can be instances where you might have to choose formula for the baby depending on the situation. And we will discuss about formula and water feeding in the coming slides.(...) But to begin with, before you get into your journey of breastfeeding, before you get your baby in your hands, it's important to know that breast milk is one of the most perfect nutrient balance which exists for the babies. It is the ideal mix of proteins, fats and carbohydrates tailored to meet precise nutritional needs of a newborn.

(...)

Immune system support, they are packed with antibodies and immune boosting components.(...) Immune milk offers unparalleled protection against infections and illnesses.

(...)

It has fatty acids for brain development which are like omega 3 and omega 6. They are crucial for brain development. And let me add two things here. The first, the immune system is something which we want as one of the primary things to be taken care of for a newborn. That's why breast milk tops the list because of the benefits of antibodies.(...) Yes, formula companies try to mimic that and put it in formula. But if we can give, even if it is a small amount of breast milk, let's say you delivered and you tried to start breastfeeding, it has started gradually, but formula has been introduced. Even then, we would highly recommend to continue with whatever amount of breast milk you can offer. Please focus on offering first milk. If first milk is possible, great. And then next, moving on, whatever breast milk you get, continue to offer that to the baby because of the antibodies it will deliver and other benefits.(...) The second point I want to mention, the fatty acid. Trust me as an adult or as someone who's working in the health industry for so long, I know how difficult the omega 3 and the omega 6 balance can be when it comes to foods.

(...)

Maybe you would have come across in your families or you've heard that people are just trying to balance this omega 3, omega 6. Some are eating fish, some are not eating fish, some take fish oil supplements. So it's a critical part, even when we grow an adult and it is found in the best balance in breast milk.(...) So I think most of us are aware that breast milk tops the list. But for these reasons, if you are in a situation even in which you're not able to give them a lot of breast milk, give whatever milk you're getting because of these benefits.

(...)

The other two benefits are ease of digestion and micro building.

(...)

Ease of digestion also is one of the things which kind of tops the list in terms of the benefits. If we have to give formula to the baby, we would of course, you know, there are different brands you could choose from and we can be as infant feeding specialists can also help you. However, the ease of digestion is something which is very difficult to achieve with formula. So on and off sometimes we have to change formula brands with babies to make sure that they are not going through any gastric problem, which is commonly seen in formula fed babies. So this information is not to put you under pressure or not to put you in any form of grade. If you have to choose formula, yes, there are formulas which we can choose from in case the baby is struggling from gas or colic. But what I am trying to say is that with breast milk and with breast fed babies, this is not really a problem which usually occurs because the human milk just has the ease of digestion with the kind of protein balances it has in them. So that is really beneficial for the baby. And the second is it really helps in micro building, in good bacteria building, which further support the baby in terms of reducing the risk of allergies or food sensitivity. Because their stomach has been nicely sealed with the micro building from breast milk, they can, we can, it has seen that it has prevented babies from getting allergies or sensitivities.(...) The benefits of breast milk and the reason I am sharing them with you are that you know that whatever effort you put in your breastfeeding journey, whatever amount of milk you get and if you are able to exclusively breast feed, great. But even if you don't get there, whatever journey you choose, whatever steps you take are so, so worth it because they are giving the baby so much more than just nutrition.

(...)

I already mentioned formula milk a few times. I know this is, this is something which commonly can happen.(...) One of the classic examples is that the mother had a C-section, so the baby and the mama had some separation and as part of nourishment for the baby, the baby was given formula milk.(...) So as new parents, it is of course important for us to know what is formula milk and yeah, is it bad? Do we need to be concerned about it? So let's go through these questions. The first, is formula feeding bad? No, absolutely not. So firstly, let's not benchmark bad or good. These words with infant feeding, especially infant feeding.(...) So formulas are not bad. They are benchmarked against breast milk. So you know, you have a gold standard which is breast milk and that has been taken as a reference and then milk has been, the formula milk has been benchmarked against it. Yes, it's the next save option for the baby. So in case of any medical or lifestyle decisions, even sometimes the mother has to transition to formula depending on some lifestyle decisions, work decisions, it's completely okay for you to make that decision.(...) And if you are able to continue breastfeeding, we would highly recommend it. So for some reason, if you are not, then yes, it is the next save option.

(...)

There is one thing I would like to add here. Sometimes formulas, formula, not companies, but the other, the people around us or the set up around us, sometimes it almost sounds like that they are talking of formula highly. As if the formula is not given, then the breast milk is not enough because something, you know, with the breast milk is not enough because it's not seen. I will cover the myths and the end. But this is one of the things you might encounter that because you can't see the baby drinking the amount of breast milk or you can't really see that transfer. You can't really see it. See it's so pure and it's so yeah, it's something so I would almost call it spiritual that you can't really see what's going on. You can't really see how much the breast milk, how much of breast milk baby has had. And as I said in my, in our intro, that's such a power that you can actually nourish a human being out of your body. So all of this because it's unknown and unseen.(...) Sometimes unfortunately questions such as the baby stomach is not getting full come for breast milk. Sometimes you know the breast milk is not enough. These kinds of comments come on these kind of questions come in those situations. Yes, we should cater to those questions. We should cater to those situations,(...) those concerns, but with the help of a professional, not just meeting, you know, not just thinking in our own head and then saying that you're the breast milk is not good enough. We have to give formula. So what I'm trying to say here in a nutshell that formula is not something which is, is, is above breast milk as if you don't give formula, then the child is going to be nutratively deficient. No breast milk is the gold standard and formula is the next safe option. So please keep that in mind. And with few points, I said whether your child is drinking enough or not, I'll cover them in the coming slides because I know we know that new parents have those questions.(...) Sticking to formula,(...) is formula, so the next question would be, is formula heavy for baby?

(...)

Formula milk manufacturers have tried to mimic breast milk composition. That's a fact, but it isn't a complete replica because it's not completely possible. So yes, some formula compositions can be heavy for babies.(...) For this, it's best to discuss the type of formula with your lactation consultant or even pediatrician if you are, if they are equipped with this knowledge at the time and see if depending on baby's need, a change in formula composition is needed.

(...)

So please keep this in mind. Yes, it can be on the heavier side as it is synthetically made. It is safe for the baby, so no, no worry there and no guilt there.(...) But yes, sometimes we might have to switch formula brands or compositions and then you need a professional.

(...)

Can I do combination feeding? Of course you can. Depending on your personal, medical and baby related situation, combination feeding is totally viable. Also during this time, it's best to discuss the process of feeding. So you would have questions such as what should I give first? Should I give formula first or breast milk first? So these are some things it's best to discuss with your consultant. I would like to leave a tip with you. If you are a breastfeeding mother, you enter into the breastfeeding journey and you're also giving formula to the baby, then specifically focus on giving the morning breast milk to the baby and the night breast milk to the baby. When baby suckles on mama's breast, the breast milk adjusts its depending on baby's need. So what does that mean? At night, the body knows that baby is wanting to go to sleep. Baby will come into the cycle of falling asleep at night.

(...)

So the breast milk becomes slightly drowsier.

(...)

And in the morning, the four milk and the hint milk, which is the front and the back milk, they all, it all combines and it is very high and rich in fat milk. So that milk, that feed is really good for the babies to have. So this is a tip to keep in mind if you're doing combination feeding.

(...)

So, in our module 2, we went through the critical period of birth, what are the capabilities of a newborn and what are they looking for. Now, we kind of know that they are looking for their mother, but how to establish that bond, how to get there, how to nurture it depending on the situation when the baby is born, how the baby is born is what we will discuss in module number 2.

(...)

The first thing, establishing the baby and mama bond.(...) I would like to read this statement. An infant suckling at his or her mother's breast is not simply receiving a meal, but is instantly engaged in a dynamic, bidirectional biological dialogue.(...) It is a process in which physical, biochemical, hormonal and sociological exchange takes place. Designed for the transfer of much needed nutrients as well as building a strong social bond between the mother and her infant.

(...)

So, what does this mean? When baby is suckling at mother's breast, they are not just getting milk. That is why I keep repeating this throughout the course. No matter how many times breastfeeding you are able to do, no matter how much amount of breast milk you are getting if you are pumping milk, as long as you are comfortable and the baby is supporting you and you are doing the breastfeeding journey, please continue to do it. Do not look at it as just a mere exchange of food. There is so much more the baby gets from the mother. And that's why I said that please, fathers, join us in this course because this is important for a family and for fathers and basically for all the caretakers who are around the mother to keep in mind.

(...)

If we look at a plant, we want that plant's fruit to flourish. We want the plant's fruit to be nice and big and juicy and you know basically flourish into, you know, whatever the plant is going to become, whatever the fruit is going to become into. For that, will we keep spraying water on the fruit? Will we keep spraying water on the leaf?

(...)

No.(...) Even if you are not into gardening, most of us know that we would be giving water to the roots. We would be giving water in the manure part, in the soil part of the plant where the roots are.

(...)

Why am I sharing this analogy? Apply the same as the mother and the baby want. Baby is the fruit of that plant, is the fruit of that tree. We all want the baby to flourish.(...) Mothers are the roots.(...) So nourish the mothers. Give them water, give them space, give them acceptance, give them no judgment, give them a lot of care so that they feel nourished and they can further nourish this little human who has come your way.

(...)

I think we all know the answer of this question.(...) What does the baby need most at the moment of birth?

(...)

Answer is the presence of his mother, the presence of her mother.

(...)

Breastfeeding typically begins right after birth, as it is the ideal time for the baby to latch onto the breast and start receiving colstrom, the first milk which is rich in antibodies and nutrients. The ideal time, by ideal time I mean the first hour. And by latching on the baby and receiving colstrom, this is the first milk.(...) However, there can be situations where immediate breastfeeding is not possible due to medical reasons or any complications.

(...)

In such cases, once the baby and mother are together, it's important to prioritize initiating breastfeeding as soon as possible. And how do we start that? We are heading towards the direction of answers of these questions basically how to start.(...) This will involve things like skin to skin contact, where the baby is placed on the mother's chest, which helps regulate the baby's temperature, heart rate, breathing while also promoting bonding and initiation of breastfeeding.

(...)

If there are any challenges or difficulties when breastfeeding, seeking assistance from healthcare professionals or lactation consultants can really be helpful in overcoming them. I would highly, highly encourage and request that in this journey, if you feel that yes, I am, you know, I want to do breastfeeding, I'm ready for breastfeeding and mostly most of the mothers feel this and the baby is also coming to you. If the baby is latching and the process is going perfectly good, then great. If it is not, then please seek our professional help.

(...)

Yes, as I said in the previous slides formulas is there. So we don't have this worry of survival of the baby, which is a great thing in today's world. However, we do want to not let go of the innate behavior, which is of suckling at the baby's momma's breast. So please, if you need any help and if you're struggling, reach out for professional help.

(...)

Firstly, whenever it's possible, whenever possible means that when the baby and the mother are coming into the same room, bring them together. So we are coming to the answers of how to initiate breastfeeding.(...) Bring them together, bring them skin to skin, as you can see in the image. So here you keep the baby only in their diaper on in their nappy and you keep them on the mother bear chest. It's advisable for the mother to be bare chest to facilitate this connection. So yes, you can keep yourself warm from the side. You can also cover the baby on top with a blanket, as again, you see in the image. And you can also make the baby wear a hat if you are a cap, if you want to face the baby specifically born in winter months. But other than that, keep them bare skin together. A good way to ensure that you're in correct skin to skin position with the baby is to gently lift your head and kiss the baby exactly what you see in the image.(...) And this happened to me in consultations where mothers are wondering if their skin to skin distance is okay.

(...)

So a way to check that is to be able to kiss baby's head like this. As long as you can reach the baby's head like this, that means the posture is good.

(...)

In terms of frequency, skin to skin basically is like a medicine. You can't can is one of those medicines you can't have enough. Is beneficial for babies, especially in the case of C-section. So here, yes, we need to keep care of the mother in terms of the stitches and wherever the, you know, depending on the severity of the cut and the kind of cut. But keeping that area protected, it is highly, highly advised for the baby to come on to the mother and do the skin to skin.

(...)

Now what will be the ideal moments? The ideal moments would be when whenever the baby is in the nap state, which is going to be quite often, try to do contact napping. Both you mostly when the baby is tired, mother is anyways tired, but mother is also gets drowsy and this helps both of them fall asleep together. And then when they are slightly waking up and you're also waking up, it's easier to initiate breastfeeding because from your chest, the baby can go down and start their breastfeeding journey.(...) Bringing them onto your chest for the last 10-15 minutes before they fully wake up can also facilitate breastfeeding. So what do I mean here? If the baby is not napping on you, you know, for some reason they nap separately and you, you know, you maybe went out, took some refreshments or took a shower, when you're back and you're, you know, you're nice and clean and you want to be with the baby, let it to be with the baby, then we would advise to pick the baby before baby wakes up. So around this 10-15 minutes of window, put them on you and then continue the nap time for the baby. Basically the baby is going to wake up because of the touch and you know, just coming close to his mother and then you can utilize that time and bring the baby closer to your breast and start breastfeeding.

(...)

These these series of events can turn slightly differently. You can, you know, they will differ depending on your situation. But what we need to remember is no matter whatever surgery we've done,(...) when there's a distance between the mother and the baby, remind yourself of the swimming pool situation. Baby has come out of water, is in air and is wanting to reach out to the surface, to grab the surface and that surface is the mother.(...) So whenever you can bring them close together,(...) slowly bring them skin to skin, which is bare chest and then depending on how the mother is feeling, how the baby is feeling, be ready to start breastfeeding.(...) If this can be done in the first hour, it's ideal. But even if it cannot be done in the first hour, we do not want any parent, any mother or father to panic.(...) If the first hour has happened, perfectly, perfectly good. But if it has not happened, it's also okay to keep the same first hour in mind. So what does that mean? It's been two hours or two and a half hours and the babies and mother has not come in contact and now the baby comes. Let's say the baby was taken to unit, critical unit and now the baby has come. Your first hour starts now. Now you bring the baby to you. So rather than just taking them directly to the breast and you know, maybe having nurses in the room, maybe having family members in the room,(...) create a calmer environment, create a calmer space, be it in your room, in your hospital room or in your, if you've come home.(...) And now when you come in contact with the baby, get bare chest, bring baby bare chest on you and you start your first hour, whatever time you get in touch with the baby.

(...)

And then slowly, slowly, you know, you keep, continue the contact nap or you keep them on you and slowly, slowly you initiate breastfeeding.(...) During this journey, a term like breast call also happens, which we will show you a video of, but that is also a common thing which babies do, that they breast crawl and they start their breastfeeding journey themselves.

(...)

In all of this, remind yourself the swimming pool example, remind yourself that the baby is fully, fully capable of, you know, recognizing the mother. They know how to suckle. They want that breast milk and mother's body also needs the baby. So as soon as they're together in the same room, bring them together, keep them skin to skin, keep, give them a lot of calm, comfort and then in the skin to skin process, go towards the breastfeeding journey.

(...)

So if you remember in one of the initial slides I showed you, that baby has four biological needs,(...) oxygenation, nutrition,(...) warmth, protection. Where does baby get all of them from? The mother. I think again, we would have now by now understood that we are moving towards mother in terms of the primary, you know, fulfilling those primary needs and the significance of skin to skin lies in that.

(...)

With the help of skin to skin, with the help of that contact, whenever that happens straight away or after some time, firstly, the baby's oxygenation supply, oxygen supply and overall breathing rate is going to stabilize. Secondly, nutrition wise, they will be ready for suckling, they will be ready for breastfeeding and their initiation of breastfeeding journey is going to start. Third, warmth, they're going to get so much of warmth from the mother and so much of love. Overall, this helps in their thermostat regulation.

(...)

And fourth is going to be the protection. As soon as they are with mother, the surface which they needed after coming out of the swimming pool is with them so they feel protected and safe.

(...)

I think by now we know that it's important for the mother and the baby to be together. How can we support in this healthy connection? How can we support in a positive breastfeeding relationship? Should be our next question.(...) The first thing which we as a family, be it the father helping the mother or the other family members helping the mother, we should encourage frequent holding, touching and skin to skin time with the baby as discussed in the previous slides.(...) I would like to emphasize here, sometimes in some of our discussions and some of our consultations, we have heard comments like we shouldn't be holding too much of the baby in our arms. The baby is going to get kind of used to of that or something around these terminologies that the baby is going to get used to, something like that. This logic, this statement does not apply to a baby. It does not apply to an infant. It does not apply to a toddler. It does not apply to a child.

(...)

If a child which is be a child of a two year or three year of age or a baby which is of two days or three days is wanting that attachment, then it's something we should give them. This is not something which is going to go in any negative form. So please, especially when we're talking about the baby and the mother bond, please encourage frequent holding without any back thought in your mind and encourage skin to skin.

(...)

Second, it's essential to acknowledge that the mother is the natural habitat for the baby. This means, what does this mean? We're coming back to the plant example. This means understanding that the mother's care needs to be a priority is very important. Families need to recognize this and should provide a positive,(...) very important, a calm(...) and a happy and nourishing environment to the mother.

(...)

This can be done only when we understand that breastfeeding is a very natural process. It takes its time. We need patients, we need care and the baby needs and wants the mama. Mama is like a chocolate factory for the baby and the baby wants to open that wrapper and have all that chocolate. So really we just have to show them the path. We just also maybe have to let them figure out the path. And in that, if they need professional help, then yes. But other than from the family and from the surrounding, they need support, calm and happy and positive atmosphere.

(...)

Third is recognizing the importance and the significance of the first hour of the delivery, often to refer as the golden or the magical hour. During this time, the baby will primarily need mother's presence and care, which we have discussed. So it's important to bring the baby and mother together as soon as possible, initiate skin contact and allow them to have a quiet and relaxed time together.

(...)

Keeping the mother hydrated and nourished during this time is also very important. This approach increases the likelihood of the baby performing breast crawl. So we're going to come to breast crawl in the coming slides. And the baby's also natural instinct to find the breast and start breastfeeding. So please keep the first hour in your mind. This goes again as a message to the family, to the fathers. Keep the breast first hour point in mind. You can also upfront discuss with your nursing home, with your clinic, with your hospital,(...) that you would like to perform the first hour. If it's a C-section, even if it's a C-section, as long as the baby is okay, can the baby come to you directly, come to the mother directly? And if it's a vaginal birth, then again, as soon as the baby is out, the baby comes on the mother directly. So this understanding is very important. And the fourth point is exploring breast crawl for a mother and a baby. This is something we are going to have a look in a video.

(...)

Before we go to the video of breast crawl, I would like to read this statement so it stays in your mind while you look at the video.

(...)

Western culture has not prepared either mothers or professionals or other caretakers to expect such infant competence. You are going to experience infant competence in the next video.(...) On the contrary, the newborn is usually understood to be quite incompetent. His behavior or her behavior is restricted by unpredictable and intrusive reflex responses, insatiable drives, and neurological disorganization. So what does this statement really mean?(...) While it is true that babies cannot behave like adults, they are not fully developed yet. However, they possess inherent competence that is often overlooked because they are small and they are still vulnerable.

(...)

They have the ability to recognize their mother to suckle and to initiate breastfeeding,(...) and we sometimes overlook this. As parents, caregivers, and society, it is our responsibility to leverage this competence and facilitate their breastfeeding journey.

(...)

Recognizing babies as just recipients of care, assuming that they know nothing and need everything to be done for them, does not empower them. I know maybe some of us are thinking, what is she talking about? How does baby have any competence? I would like to refresh your memories of the slides we went through. They have competence such as recognizing their mother with smell, with touch, with feel. They have competence of suckling. They also have competence of initiating breastfeeding. We completely understand when this new little flower comes in our hands, it is very vulnerable and we do believe that we need to do everything for them. While it is true, we do need to prepare things for them, but more than doing things for them, we need to facilitate the things for them. We need to create an atmosphere which is protective, safe, and warm for the mother so that the mother can further support the baby and lead them into the direction of breastfeeding and bonding with each other. With this note in mind, with this point in mind, let's look at the next video.

(...)

How beautiful was this video?(...) It's a small clip. The mama and the baby were together for approximately 30 to 40 minutes before the baby did the breast crawl and latched to the mother. However, we only see a small part of it in the video. But even in this small part, did you notice that the baby is kind of moving from breast one side to other side, kind of figuring her way out. She's lifting her head and then moving her towards the side, lifting her head and then moving herself again to the side. This is what we call the breast crawl.

(...)

And what is the competence? The competence is firstly that the baby knows that I am on my mother and that's because of the fragrance, her smell, her touch and her love, her warmth. The second competence is baby also knows that I would like to have food now. I want to find the breast. So baby is searching for the breast when the head is going from one place to another. And the third thing is finally latching on to the mother. So the mother is lying down and this is a video just after birth. The baby is wearing cap but the mother is bare chest and the baby is also bare chest. And here we are performing skin to skin which was done for approximately 30 to 40 minutes. And given the chance the baby was able to adjust,(...) almost crawl and kind of lift her head and then move, lift her head and then move and latch on to the mother and start her breastfeeding journey.

(...)

This is one example of starting breastfeeding journey. Even if you feel that you're not into the breast crawl group and you would want to latch your baby straight away, we would still highly recommend to follow the following steps. The first, as soon as you can, bring the mother and the baby together. Give them some time alone on each other. You can still be with them but create a calm and quiet atmosphere around them.(...) Then depending on the team you have around you, be it the nurses, be it the lactation consultant or be it the midwives and the gynac, then bring the baby close to the mother in a way that they're getting ready to start their breastfeeding journey. To do that, please start with skin to skin. Please keep them on each other for some time, bare chest so the baby can make that connection and the mother also. And once that happens, you can slowly bring them towards your breast and start the latch or you can give them this time to do the breast crawl. Whatever method you choose, either you latch them on to the help of professionals and yourself or you do the breast crawl, please do perform skin to skin. Give them quiet and calm atmosphere together. Let the mother connect with the baby. Probably there's going to be tears, there's going to be happy tears around. Let that happen and do the phenomenon, perform the phenomenon of skin to skin and then you would see magically how baby is going to come closer and closer to the mother.

(Gentle Music)

(...)

Moving into our module three. In module three, we will delve further into practical aspects of initiating breastfeeding once the baby and the mother are together and have established skin-to-skin contact.

(...)

So far in module one, we went through different capabilities of the baby, what the baby wants and needs, and what we should be prepared to offer them. In the second module, we went through the emphasis of the baby and the mother coming together so that as a family, we understand this. And now in this third module, we will go through some tips and tricks, basically how to accomplish it. We will discuss how to prepare ourselves and the environment to ensure both the baby and the mother are comfortable and supported during this sensitive time of getting together. Specifically, we will explore the steps to take when the baby is in our arms and about to start breastfeeding. This will include techniques for positioning the baby at the breast, ensuring a proper latch, and recognizing signs of successful breastfeeding. We will also address common challenges that may arise during breastfeeding and provide strategies for overcoming them.

(...)

While focusing on the practical aspects of breastfeeding initiation, we aim to empower caregivers and parents with the knowledge and skill they need to support the breastfeeding journey effectively. This will contribute to the establishment of a strong bond between the mother and the baby and promote optimal infant nutrition and development. So let's get started.(...) The first steps when you are ready to start breastfeeding.(...) Whether you follow breast crawl, which is putting the baby's skin to skin and let the baby find the breast and latch themselves, or you directly latch them to your breast, please do these few things. The first, do not wipe your breast or clean or take a bath before the first latch. This is something very important to keep in mind.(...) Our breasts around the nipple area and around the darker area, which are the monochromary glands, secrete oils, secrete fragrance, and have that feeling of home for the baby. These smells and these fragrances are familiar for the baby, and we do not want to wipe them off and make it difficult for the baby to find them. So please don't clean or wipe your breasts before the latch, before the first latch. Also don't take a shower. You can start taking bath after your first latch or maybe after a few latches, but you still don't need to clean your breasts before every breastfeeding session. Please keep that in mind.

(...)

The second, keep the varnix on the baby. Varnix is this waxy substance, which you see on the baby slightly, the wipe structure, which you see here on the baby's cheek. And on the neck, if your nursing unit or your hospital or your gynec are open to having this conversation, then you can also ask them that you wish to not remove the varnix from the baby. Sometimes the healthcare institution will do it, depending on the weather also. That's okay, but if it's possible, please leave it on their hands, because this way they have this waxy substance, which is coming from the womb on them, and this fragrance and this feeling is similar to the nipple area of the mother. So both of these basically will tell the baby that here my food is.(...) In this instance, I personally like to take an example of coming home from school. So whenever I used to come home from school, I would just knew what is there in lunch based on the fragrance. As soon as I entered the house, I knew my mama has made this. We have a dish which is made of kidney beans. We call it rajma.(...) We most or most of the kids love it. So whenever my mama used to make that, and I used to enter the living room from school, I would just know it instantly because of the fragrance. We apply the same logic here for the baby. The baby will be finding his mama and his food or her food for the first time. So let's keep that fragrance.

(...)

I would repeat the sentence I mentioned earlier. The varnix and the Montgomery glands, these are the darker parts of the nipple around mother's breast have similar smell to the amniotic fluid. Amniotic fluid is the fluid in which the baby was in the womb. So we want to keep it. And the last thing and the last point which we want to do, I think most of us can guess it by now,(...) skin to skin. I am saying this with a smile because I really want this imprinted in all the new parents' mind that skin to skin is a medicine we want to perform and eat and activity do every day as long as the mother can do it and her body allows her to do it. Please consider it a prerequisite. It is a mandate to do before you get into breastfeeding. So please keep these few things in mind.

(...)

Moving on from things we should not be doing to things we should be doing to ensure that we get a good latch.

(...)

The first thing I would encourage every new mother to do is to familiarize yourself and connect yourself with your new body.(...) With pregnancy and with the delivery, you would notice changes in yourself, changes in your body which are part of the journey. So in this change, it's important to connect with the new you. There's a lot of connection going on when the baby comes out and this includes also connecting with your new self.(...) So what do I mean by that? Familiarize yourself with the changes in your breast. Touch your breast, see whether your breast, where are your breast growing? Have your breast gone slightly on the lower side so has the heavy side gone on the lower side or has the heaviness taken them on the side? In both the cases, it's important to note this because this will help you to support your breast when you are breastfeeding.(...) So what do I mean by that?

(...)

When we start the breastfeeding journey, it can be that your breast are slightly heavier for the baby to find the nipple. And then when that happens, we can support our breasts, lift them slightly and give them that support and then guide the baby towards the nipple. If your breasts are slightly on the smaller side, but they've moved on the lateral, on the sideways, then you can hold the breast like this. This is the C section. This is another C section, sorry, this is the C shape. So in the C shape, that means that we support them like this as you see on the image. If your breasts are on the heavier side and they've gone on the droopy side, on the lower side, then we support them and uplift them with a U-hold. This is a U-hold as you see in the slide. So please, first thing is to familiarize yourself with your new breast. The second is to connect with what kind of shape you need to hold them with, be it with a C shape or be it with a U shape. The third point is going to be fingers of the dinner plate. What do I mean by that? When we offer our breasts to the baby and when we are supporting our breasts in the U and the C, and there's a lot of new stuff going on, sometimes I'm going to show you with a dummy, sometimes when we support the breasts, so let's say like this, we support them almost from here. Just, you know, if you can see it closely, we almost cover the glands. We also, you know, we're kind of almost touching the nipple. Please keep in mind that not just the protruding part is the nipple, the entire, this part is the nipple. And these small, small, small, small bumps, which you see, these are the montybomary glands. This entire part is where the baby will connect.

(...)

And this part, when we hold them in a C form, sometimes we cover with our fingers, we cover our nipple. We do not want that. So we want mothers to hold from the back so that the nipple area, this entire area is completely free for the baby to come and latch. So please keep these points in mind.

(...)

And lastly, babies will of course be breathing when they come to your breast,(...) when you latch them. Sometimes mothers are worrying that they need a breathing hole. As long as the baby is in a nice latch position, comfortable, you see them, you know, they are connected with the breast. They don't specifically need, you don't specifically need to, for example, you know, just stop your breast like this or cover your breast like this so that the baby is, you know, able to breathe. They don't really need a breathing hole like that as long as they're latched correctly and the position is good for you and good for them. Now we know what points we need to keep in mind to ensure that we are able to form a good latch with the baby. Now in this process, we would also like to assess whether the baby has been latched correctly. There are visual cues that both the mothers and even the fathers can observe. And these indicators will help you determine whether the latch is good and if breastfeeding is proceeding effectively.

(...)

The first is going to be an asymmetrical latch. So this may be sounds counterintuitive, but we don't want a symmetrical angle for the baby. We don't really want a very symmetrical latch. We want a proper latch does not need to be perfectly symmetrical. Instead, we want it asymmetrical. This means that the baby's mouth is going to be slightly off from the center of the breast and it will rather than in the middle and they will latch themselves from the lower part. So what do I mean? I'm going to show you with the dummy again. So we have the breast and we're going to consider, consider my hand as lips of the baby. When the baby is going to latch, the baby is not going to latch completely like this in the center. The chances are that your breasts are gonna be droopy like this. You're gonna keep the baby's mouth like this and they are going to latch from the bottom to up. So they're literally going to latch from here. They're gonna hold the breast from here and then form an asymmetrical latch like this. This is how they will get the entire nipple in the mouth. As this is the dummy, the nipple is quite small with new mothers, the nipple is slightly on the bigger size. So when they latch, we want it to be an asymmetrical latch. So from here to here. So they're not directly gonna come and just only attach to the nipple. That is the first point to keep in mind. The second is that there's going to be a wide gap of lips, at least 140 to 160 degrees. I'm going to show you two images and you'll be able to understand completely what I mean by the gap. The third is that there's going to be, these are gonna be flanged lips. This is also something I'm going to show you in the image. When you will experience this asymmetrical latch, a gap of a wide lip and also flanged lips, you will be able to almost be assured that there's effective milk removal. What does that mean? That you will be able to be a listen to baby in a rhythmic form,(...) sip, sip, sip, swallow. And this rhythm, you'll be able to basically see it or hear it. This is one sign that is effective removal.(...) And the second sign is once the baby is latched off, the baby will be nice and calm, not fussy. And you will also feel your breast quite lighter. Overall, it will be a comfortable experience for you. Now let us look at the images.

(...)

This is the first image. As I said, we do not want a symmetrical latch for the baby. Here, if you notice, the baby is latched very symmetrically right in the center. That's not something which is going to give them effective removal of milk. So when I say we want an asymmetrical latch, what do I mean by that? I showed you technically, but internally what we mean, that asymmetrical latch will help them to form the right angle and the right hold of the breast, being able to form a vacuum in their mouth with which they actually do the suck and the swallow rhythm.

(...)

This, as you see, I'm going to also circle it so you can basically see it on the slide.(...) Here, if you notice,

(...)

this is a very firstly symmetrical latch. We want an asymmetrical latch. And second, you would notice that the angle of the lips is not white. It is quite small. This is exactly the, we want exactly the opposite of this. We want a wide angle. So these two are the first signs that the latch is incorrect. The second, the third sign is, as you can see, that baby's lips are on the inside, like this. We want the lips to be on the outside. So literally like a pout. We want the lips to be flanged on the outer side and not on the inside or contained. Right now, they're quite contained. So these three signs are pretty much visible that this is not a very incorrect latch from the lips area. The second is, the second area which we can notice is this part.

(...)

Do you see the baby slightly in strain? You know, they have like a frown on almost on their face. We can see that the baby is tensed and it's quite an activity for the baby to suck the milk out. We don't really want this. So what we want is actually the opposite of this. (Keyboard Clicking)

(...)

Let us look at it in the other image.

(...)

This, this is what we're looking for. Here, what do we see? Firstly, we see,

(...)

I'm going to show you in different colors.(...) Firstly, we see an asymmetrical latch. We see a nice big mouth here. First, they grasp the lower part of the breast. That's how it goes very quick. It's not the first and second, but yeah, we want the grasp to come from low to top. And then you see a very nice, you know, open latch, asymmetrical latch on the top.

(...)

This is the first thing. The second thing I would like to highlight is going to be the angle. So if you see this angle,

(...)

it is a wide angle, you know, approximately 142, 160 big angle. And that's what we're looking for. We're looking for an octuse angle, a big, nice wide angle.

(...)

That's the second thing.(...) And the other thing, which we see,(...) I'm going to make it nice and green. We see a nice, calm, relaxed baby. This is what we want. We want the baby to have a nice big open mouth, asymmetrical latch, relaxed, not stressed, and another thing, what we're looking for, I'm going to show you around the mouth area.

(...)

Another thing what we're looking for are the lips. You see the lips of the baby.

(...)

They are on the outside. They are flanged. They're not on the inside. So these are some critical points to look out for.(...) And this is one of the most important slides we have. So I would highly request again for the fathers, for the caretakers, for the families to see, so that you know and you're prepared that this is what we're looking for in terms of a good latch. In this entire process, of course, there's 0.1, 0.2. All of this goes very fast and all of this goes in a symmetry. So please connect these points with each other. And one of the best indicators is you yourself.

(...)

If you are in pain, it's not good. If you still feel your breath quite heavy, slightly hot, or you feel, you know, some kind of clottish bit around your breast, it's not right. So these are the signs to look for. And we'll further discuss this topic in the coming slides.(...) So after looking into the points, how do we know that the latch is good, or we ensure the latch is good, it's important to look at. How do we know that the latch is not good enough and we need or we should seek some professional help? The first is, as I said, we're not gonna start with the baby. We're gonna start with the mother. The mother is in pain.

(...)

Let us please not normalize pain, pain with breastfeeding.

(...)

Sometimes with a latch on and off in the beginning, mothers can feel slightly pain and that's not gonna be just around the breast. These are also called post delivery contractions, which is around the uterus area. As the baby sucks, the uterus also gets smaller in size. Those are post delivery contractions. That is separate, that is different. We are not looking at mothers to be in pain when they are breastfeeding. So let us please not normalize pain when breastfeeding.(...) The second is that the baby will not be receiving optimal volumes of milk. But how do we know that? Firstly, we would know that the baby is not gonna be very happy after the feed. They're gonna be slightly fussy or you know, unhappy. And you won't really see a very content, you know, nicely drunk baby. No, when we have a milk drunk baby, we can just see it in them. We will not have that, you will not see that with the baby. You would see a slightly fussy, unhappy baby. That's one indication that the milk was not optimally transferred. The second is the baby is gonna be snacky. So gonna be sipping, drinking and then off. And then after 30 minutes or 40 minutes coming back again, so that's a very snacky baby on, off, on, off going on.

(...)

You as yourself, as a mother in terms of the breast, you would feel that they're not gonna be a nicely drained. And you might also feel that the heaviness you were feeling is slightly distorted. So you don't really feel as heavy or you feel slightly more heavy. On and off this on and off confused feeling will give you indication along with pain, will give you indication that this is, the latch was not good enough. Sometimes this leads to decrease in supply and also plugged ducts.(...) The situation should hopefully not get that far. But for it to not get that far,

(...)

I would highlight the image again. You see here the baby, remember this. We're not looking at a symmetrical latch. We don't want a frown baby. We are not looking at lips inside. And we're also not looking at a very small angle. When a latch is like that, the chances are that either you would be in pain or you would, the baby after unlatching would be fussy or you would feel yourself that the milk was not nicely drained, nicely given to the baby. In any of this situation, in any of this condition, we are looking at professional help. You can always switch to include formula or switch to formula or do combination field. But we would highly encourage to first get professional help, figure out the solution and then decide which way you need to go. So as we went through the previous slides, it is clear that it is crucial to understand how to achieve a good latch, recognize the signs of a good latch and identify the signs of a poor latch so that you know that some help or some correction is needed.

(...)

However, in this entire process, we do need to also understand our baby.(...) We need to understand whenever baby is ready to feed. And by that, I mean we need to understand their feeding cues.

(...)

Cues are signs, indications, which they will give, which if we understand or start understanding as new parent, we will be able to have a baby lashed on the breast and start breastfeeding much sooner.

(...)

So the first thing to keep in mind is whether your baby is handed to you immediately after birth or has spent some time in the new night care, before coming to you, the breastfeeding usually has started. What that means that they are ready to start to suckle, they are ready to come to you, they are ready to come skin to skin. This is important to keep in mind. It sounds something very small, but it's kinda like just take a different analogy. They know you, they are already in love with you, they've already had that, you know, love at first sight kind of feeling. Now they just want to come back to you. So that connection, that desire to be with the mother, that desire to be close to the mother is already something which the baby has. Be it the baby was with you straight after birth or be it they come to you after C-section. That is the first thing.

(...)

As part of the feeding cues, these are the indicators which will tell you that your baby is ready for feeding. So what is the first cue? The first cue is going to be rapid eye movement. This is literally like looking for food, almost like, you know, here, there, like we look for someone,(...) we're reaching out for someone, it's the same thing. The same way the baby will do rapid eye movements in order to look for you. This is similar to kind of when we come home from school. And, you know, I've given this example earlier, but literally when I used to come home from,(...) you know, when I used to come home from school, I would just look around for my mother. And I would just say, even if I saw my father,

(...)

I call him Papa and say, even if I saw my Papa, I would say, Papa, where's Mama? That's like the first look, the first thing I would look out for. So this is very common. This is something we even do now. This rapid eye movement basically means that they're looking for you.

(...)

When you notice the rapid eye movement, it is a sign that they're searching for food and it's a perfect moment to bring them skin to skin. If you can bring bare chest, then great. If you can't bring depending on where you're sitting or depending on, you know, maybe you're in a different room, please do bring them to you on your chest here. So even if you're not bare skin, plus please keep them here on your chest around this area and then slowly start bring them down and bring them closer to latch.

(...)

The second cue is going to be quiet and alert time. So it could be that sometimes we've missed this, you know, rapid eye movement, but the baby has woken up from nap and they're quiet and they're alert and they're wide open with their eyes. This you would notice, new borns do this. They will go like wide open with their eyes and they start looking here and there and they're quiet and they're quite alert. That moment is also a sign that they're ready and they're looking for food. In neither of these signs, the baby will cry. These are not crying signs. These are quiet alert signs.(...) Now you would start seeing them doing some activity. This activity is called rooting, which is basically this, this, this, this. They're gonna start going towards their arm. They're gonna start going towards their fist. This also means that they are ready for food. Mostly we recognize this sign, but if you notice in the list, this is the third sign. And after rooting straight away within an instant, they're gonna start crying. And sometimes the crying starts slow. Sometimes the crying is loud and clear that I want my food.

(...)

Crying and shouting and, you know, wanting food, crying for food is the fourth sign.(...) So as you see, this is the last sign. This is the last feeding cue. Of course, we want to give the baby milk, you know, as soon as they're ready. But sometimes this as soon as they're ready is missed in terms of the rapid eye movement, REM in terms of the quiet alert time. Mostly when we react is the rooting time or the crying time. And sometimes these are the reasons why the latch becomes difficult because they are quite hungry. So please keep this in mind as new parents that when your baby has woken up from a nap, it's been two hours, one and a half, one, two and a half, or three, whatever the duration has been.(...) And they are showing signs of, you know, just with their eyes open, they're showing signs of being alert, but they're quiet. Bring them to you, do skin to skin, and slowly move them down and latch them.

(...)

If you miss them, it's okay. Slowly you will get a hang of these signs. Of course, the baby's gonna cry and tell you anyways that they're hungry, but slowly and gradually you're gonna get a hang of these signs.

(...)

So as part of our course during our live session, we have incorporated a workshop where we will go through different latch positions. I would also say this, mention this, and mention different latch positions in a coming slide. But we feel that rather than going through every latch position like this online, it's important to do it face to face physically.

(...)

So I will cover what to bring during the workshop in the coming slide. But what I want to mention here, that yes, it's important to understand the latch positions. Firstly, it's important to be with, for the baby to be with the mother. Be in a skin to skin space, be in for the mother to be comfortable. Then it's important to know how to lash the baby, what are the right latching signs, what are the not right latching signs, and also it's important to know different latch positions. But while we get there, we just went through the feeding cues, how to know that the baby is ready for waiting. In all of this, in finding out different latch positions, there is a fundamental proper positioning hack, which I would like to share with you in this slide. No matter what latch position you choose, it's important to first apply this principle of proper positioning of,

(...)

as you see in the image, always supporting baby's neck, nape area, and their spine area. So we always give them support in this area because this is quite soft and quite vulnerable, and their muscles are not fully developed here. As the muscles are soft and delicate, they need extra support. So part of proper positioning, the mother's fingers should span out from the ear, as you can see, and I'm gonna show you here, with my neck, they should span out from the neck. We don't need to hold their neck, but just as a reference, span out from here, support their neck, support their nape, and also support their spine, and you're pretty much able to do that with your entire hand. And with this, the baby gets quite comfortable. This is the first principle to keep in mind. And now, however you hold them, be it you support this, you support it with, you support them with your elbow, or you're giving that support with your hand, with your entire hand, you will be able to latch them in any of the positions as long as this trio of ear,(...) nape, which is the backside of the neck, and the spine are supported. Then they feel quite comfortable, and it's easy, it's relatively easy to latch them. This is the hack to always remember.

(...)

Different latches positions we will cover in the workshop, and I will share more about that in the coming slide.

(...)

After applying the first hack of, or the first principle of proper positioning, which is supporting baby's neck and spine, the next step is to bring them in a sniffing position. This sounds cutely funny, however this is a great thing to do. In this position, they're not exactly latched yet. Instead, we are allowing them to smell the food. It's the same concept, it's the same concept that we've come home from school, and we enter our room, we're looking for our mother, and we smell the food, like my mother used to make kidney beans quite often, we call them rajma. As soon as I came home from school, I would say, "Where's Mama?" And I would smell, and I would know what's there for lunch, and I would already be so hungry. So this is similar to the baby recognizing mother's smell capabilities. We are leveraging the capabilities of the newborn.(...) So similarly, baby can recognize their mother's smell, and as mentioned in the earlier slides, they will be able to connect with the food through the scent. Therefore, it's important to bring them in a sniffing position, so that they can smell the mother and the breast.

(...)

It's going to look like something like this. The baby is literally in front of the nipple, in front of the entire nipple, not just the tip, but the entire areola, all the Montecomari glands. This is the entire colored part of the nipple. So the baby is close to them,(...) and as the baby comes close to that, to achieve this, what we want, we bring the nipple closer to their nose so that they can sniff it. And when they sniff it, they know that they're coming close to the food, and they will open their mouth. They will open it quite wide, big, and usually when they open it, we offer them the breast from the lower part to up. And that's how we will get the asymmetrical latch. I will cover that in the next slide, but this is something, this is something as a progression we need to do. We need to decide our latch position. We will cover that in the workshop. We need to know that we need to position them nicely and support them nicely around this area, with our hands coming across the neck like this. And when we do that, we bring them closer to us. We let them sniff the breast,(...) kinda just get ready for food. And when they're ready, they're gonna open their mouth and we will achieve an asymmetrical latch, which I'll show you in the next slide.(...) So let's discuss the asymmetrical latch.(...) As I mentioned earlier, when we bring the baby into the sniffing position, supporting their neck and spine, we have to wait for them to open their mouth wide open, which usually they will. And as soon as they open it, they will latch on, as you can see, to the lower part of the nipple forming an asymmetrical latch. The asymmetrical latch is important because it allows for the milk to flow when the tongue is down and the vacuum is at its maximum. So what does that mean? That when the baby, I'm going to show to you

(...)

with a color.

(...)

So you see here, this baby is forming,

(...)

is attaching

(...)

with the mother from the lower part of the nipple. And as you can see, it's pretty much going to open the mouth and going to go from here

(...)

and latch onto the entire nipple. This is what we call this angle, is what we call as the asymmetrical latch. When this happens, the cavity, which they form inside, we'll also show this to you in the coming slide,

(...)

the cavity and the kind of grip they form inside allows them to make the maximum amount of vacuum, allows them to make the maximum sucking power, allows them to use their maximum sucking power. And of course, with this, their tummies will get full and they will be able to receive optimum milk from the mother.(...) These two angles, when lashed nicely in terms of the mouth, are going to look like as the image on the right, are going to look like this. The lips are gonna be flashed, the angle is gonna be asymmetrical and is going to be a wide open angle.

(...)

During this attachment, there's no creasing of the nipple by the tongue or the heart palate. This also ensures that the mother will not experience any pain. So this is not just important for the baby, but also for the mother. With an asymmetrical latch, it's quite rest assured that the mother's nipple will not be creased and will not experience any pain.

(...)

And with this, the baby will also be able to receive optimum access to all the milk ducts in their mouth, and they will be securely attached to the nipple in this format. Otherwise, if the baby only attaches to the top part of the nipple, so when I say top part of the nipple, what do I mean?(...) I mean this part.(...) If the baby only attaches to the top part of the nipple, then the chances are firstly, it will be painful for the mother. Secondly, they will not be able to have all the milk ducts in their mouth. They won't be able to form the maximum vacuum. And lastly, because of this, they will not receive optimum milk.

(...)

So that's why we highly encourage for the lips to be flanged, flanged, you know, on the outside, as you see, we have to circle again the lips here as well. As you see, the lips of the baby here are on the outside.(...) They are not inverted,(...) not this,(...) more this. We want this when we achieve an asymmetrical latch, when it is at a wide angle and the lips are flanged, they are not inverted. We are looking at optimum transfer of milk from all the milk ducts into the baby's mouth. They will be able to make good vacuum, which they can handle themselves, and they'll be able to suck nicely, drink nicely in this entire latching, sucking rhythm. The mother will not be in pain. She will be comfortable, and she will not also get any nipple damage. So please keep these pointers in mind, specifically when you're latching baby for the first few times.(...) As we said in the previous slides, we would show you how a breast nipple looks in baby's mouth and how a bottle nipple looks. The first image is the breast in baby's mouth and the baby's at rest. And the second is with the bottle nipple in baby's mouth.

(...)

Firstly, you would see in the breast, because of the shape of the breast and how the baby latches, that's the asymmetrical latch, and baby always tries to take more of the nipple in the mouth with an asymmetrical latch, the baby will nicely form a vacuum, suck from the breast, and the breast nipple will go a little bit deeper in their mouth.(...) Versus the bottle, you would see the bottle nipple will stay slightly in the front.(...) So this is something to just keep in mind, that this is a primary reason why we always say that the baby should be connecting with the entire nipple and not just the top part of the nipple, but the entire areola, the entire colored part, with the montmorillonie glands also, some of them going in their mouth and the nipple also going in their mouth. The reason for this is that there are numerous milk tubs and all of them will be basically like, it's like a shower in their mouth, a beautiful shower of milk, and all of them will be showering milk in their mouth. So they do need to get a decent area of the nipple in their mouth. Versus when they take the bottle in the mouth, there's only one, you know, there's only one opening, there's only one hole in the nipple, and only that region goes into the mouth.

(...)

One of the things which is important, which we want to communicate via this slide, is the different marketings of the bottle companies. You would see that some of them market that this is the best nipple because it will not create any nipple confusion. This is the best nipple because it is as close to breast. This is the best because it is as close to breastfeeding. We will cover different types of bottles in the coming slides.(...) But what we want to say to you here is that no marketing of the bottle is really affecting how the nipple is going to interact with the inside of the baby.(...) Yes, the bottle, the bottle size, the bottle flow, the nipple size, the nipple type, texture, this is going to reflect on how the milk goes from the bottle inside the baby's mouth. But when the nipple is actually in the baby's mouth, that nipple stays unaffected, depending, you know, no matter which bottle you choose. Maybe some will go slightly deeper, maybe some will go slightly on the outer side. But the thing what we can, what we need to keep in mind is that we can't really change the inside. We can manage how to offer the bottle, which will we will cover. We can select some better bottles, which again we will cover in the slide. But in this slide, what we want to communicate is that what we can manage is how we latch the baby to the bottle.

(...)

It should be very similar to the breast. So what are we looking at? Firstly, we don't want to say that baby should not be fed with the bottle. That's not at all the case. If it is needed, please go ahead. However, it's important to keep in mind that both when we are looking at breast and we are looking at a bottle, with both we want to have a wide open mouth of the baby. We want to have an asymmetrical latch as much as possible. And we want their lips to be flanged.(...) In these both, in both of these cases, it will be important for the baby to have an effective connection with the nipple, be it the breast or be it the bottle. When there's an asymmetrical latch, their mouth is widely open. With bottle, it won't be as asymmetrical, but still we want the mouth to be widely open, the lips to be flanged, and to have a wide angle between the mouth and the nipple. With this information, we'll move on to the next slide, where we will talk about different types of bottles.

(...)

So how do we choose the right bottle and nipple for our baby? If we are opting for formula feed, combination feeding, or maybe we are giving them pumped milk from the bottle.

(...)

Selecting the right bottle and nipple is quite a primary task. It is equivalent to breastfeeding.(...) That's why it's important to pay attention to small details, starting from the nipple shade. There are many bottles in the marketing. All of them claim to be as close to breastfeeding. All of them claim to not create nipple confusion. However, that is not entirely correct. Some of them do,(...) can create nipple confusion, or some of them are not as effective in baby's mouth. So what do we mean by that? Firstly, what we are looking at in terms of a bottle is a bottle on a nipple, which offers a slow flow. We don't want a bottle or a nipple, which is going very fast in their flow. We want it slow, and we want it, the milk to drop, drop by drop. What does that mean? That if piece, I'm going to show you a dummy bottle.(...) So this is your bottle. And if you do upside down like this, the milk comes out, the milk should be dropping one by one by one. We are not looking at all the milk to go straight away out. What we are looking at is a slow flow. That's the first thing. A very big flow is something which the baby will get uncomfortable with and gassy with. The second thing is to consider wide and slightly open mouth nipples, which are easier for the baby to suck from. So as I said in the last slide that we will cover different nipple types. It does matter, as you can see in the image here. Here, I'm going to circle it.

(...)

You see this?

(...)

How baby's mouth is nicely wide open. This is a nice, wide, big angle. So that's the first thing we want, that they are able, there's nice space for them to basically attach to. In this, in keeping this point in mind, sometimes some bottles also have slightly protruding nipple. Even that is okay. So what we want either to be have a wide angle and as a nipple, or we want the nipple to be slightly elongated. So it's nicely fits in their mouth.

(...)

Both of these nipple types are very easily available. There are different brands who have them. No matter whichever you choose, we will firstly encourage to keep the latch pointers in mind. That is the asymmetrical angle, flanged lips, and then big open angle,(...) big wide open mouth of the baby. And the second thing what we would recommend, which is something just important to keep in mind, is that even if you're doing bottle feeding and not breastfeeding, we want your baby to be with you. We still want the skin to skin concept, even if it's not fully skin to skin, we still want the baby to be in your arms. We still want that you, you know, there's love going to the baby, there's care going to the baby when the baby is latched, even if it's happening at a bottle nipple. So now that we went through different types of bottle nipples, and how does a bottle nipple interact with the inside of the baby's mouth? Let's look at how to bottle feed. We would also like to cover this in our workshop in the live session where we will meet each other, but I will show you some steps today. The first thing is bottle feeding can be done with pumped breast milk or formula. So this, if it is done with formula, we call it combination feeding. If it is done with breast milk, then it's breastfeeding and bottle feeding. But technically, all of this is fine depending on your situation, preferences,

(...)

and medical discussions.

(...)

With bottle feeding, the type of feeding which we recommend to follow is called paste bottle feeding. So what does that mean? Firstly, I would do a recap. We would want our baby in a nice and comfortable position. We would want to stay with the baby. So please do that human contact and that, you know, love and flow of warmth and affection to the baby when you're feeding them bottle.(...) And then now when the baby is with us, we select our bottle, mostly we would recommend to select a wide,(...) base wide nipple bottle so that the baby is nicely able to latch onto the bottle, connect with the bottle with an asymmetrical leash, latch and flanged lips and a wide open angle. With all of these things in mind, I would show you with my sweet baby dummy here.

(...)

So as you can see that I have the baby with me. So firstly, what we want is what I showed in the video. We want to support the baby's neck and we can use the baby's ear as a reference and their spine. We can do that with our hands or we can also do it in our elbow here so that they are nice and comfortable and they are nicely supported.

(...)

In this, we have the baby with us. Now I'm going to pick up dummy bottle.(...) So we have the baby bottle and we wait for the baby to open their mouth and then we latch the bottle onto them.

(...)

If we are doing like this, what you see? That we have the baby nicely supported with the neck. However, we have the bottle's angle like this. Almost, it's not perpendicular, it's not vertical but it's closer to being vertical. Then this will be quite a heavy flow, quite a strong flow for the baby to manage. This angle, this vertical-ish angle is not something what we want. What we want is a paste-bottle-feeling angle where I'm going to look at the bottle angle where rather than keeping it this high, we are going to bring it more horizontal to the baby. So if you notice the difference, from this angle, I went to this angle. This angle is more horizontal to the baby, is more horizontal to baby's body. Now you might notice that you might feel a question that how is the baby going to drink? For the baby to be able to drink, the angle which we lost in the bottle from here to here, we are going to kind of give that angle to the baby. So we are going to slightly lift the baby, still supporting their neck. So wherever we initially were, we were here and here. Now we've moved from this bottle angle to horizontal and we've lifted the baby slightly up. So whatever angle we lost with the bottle, we actually gained with the baby. And what we do is we do paste bottle feeding. What does this mean? With this bottle, you would see that the nipple is going to fill, when you do this, you'll be able to see that the nipple is going to fill till the end. So we want the tip of the nipple to be filled with milk, but we don't want the entire nipple to be filled like this. We want it like this, paste.(...) So the tip of the nipple will have milk. However, the end will remain slightly open, giving the baby enough time to suck. They will use their sucking power. We want them to use their sucking power because that's what something with bottle, there's something with bottle feeding we need to be slightly more conscious of. If we do like this, the baby is slightly lying down and the angle is like this. The baby doesn't need to suck much. It's just gravity is going to do the work. However, what we want, we want the baby to suck. So we bring the bottle horizontal and we bring the baby up and then the baby will need to suck.(...) And one of the classic ways to know that you are right is that you'll be able to look at the bottle and see that the tip of the bottle will be filled with milk, but the entire nipple will not be full of milk and the baby will have to use their sucking power(...) from their cheeks and from their tongue, making a vacuum in their mouth.

(...)

So this technique is called paste bottle feeding where we don't rush the bottle into baby's mouth in terms of the angle and in terms of the flow of the milk. We take it slow and we, rather than keeping the angle like this, we keep the angle slightly horizontal and let the baby suck the milk from the, or the formula from the bottle.

(...)

Moving on to our module number 4, basics and positionings. We have gone through different stages of breastfeeding. Starting with not breastfeeding actually, starting with how to lay the foundation so that the mother and the baby come together. The first hour, the golden hour, the mother and the baby bond, skin to skin contact and so much more. As we get into latch, we went through baby's angles, we went through the techniques we should follow, how we would know a latch is good, not good, how we would know our baby is ready to feed or not feed. In this journey, you might also go for pottery feeding, be it with formula or pumped milk, so we cover different types of potters which we recommend and what kind of angles to follow when feeding bottle and also when through paste pottery feeding.(...) Now that we know our foundational information, we will have the baby onto us and latch them. Here, we will cover some basics behind it and we will also re-discuss the moments when the latch is not good and when we should seek out for professional help. So, let's get started.

(...)

There are different types of positions, there are different types of latch positions holding the baby positions you can follow in order to get a deep and an iterative latch. Their names are motherlet latching, football or clutch hold, cross cradle hold, cradle hold, side lying and infantlet latch. All of them have their own, you know, their own likings, their own comfort zone. We understand that it can be tricky that which latch is perfectly good for you, which position is perfectly good for you. So, what we are going to do rather than keep it only limited to theory, what we would like is as part of this course, we would do a live session and a workshop where we will go through approximately 15-20 minutes, where we will go through the prep and practice for all these positions.

(...)

So, depending on, you know, the day which is allotted for the workshop, which you will get in your inboxes, we would request you to please come up to come in the session and please come with a cylindrical shaped pillow.(...) Together we will practice these positions, I would have my dummy baby here and you would have your pillow,(...) which you can use as a reference and we will go through different positions. Please keep in mind that one position will suit one person, another would suit another, but we would cover them all because as you go through your breastfeeding journey, you won't be sticking to just one position.(...) You can move from a football hole to a side lying, you know, latch to also an infant led latch. So, they keep changing depending on the scenario you are and depending on the experience you have gained in your breastfeeding. So, for this slide, we would take this further and discuss this further in our workshop, in our live session, which you will receive information in your inboxes soon after the course.

(...)

We understand that during this journey, there can be chances, there can be situations when the latch is not correct. I shared this in the first half of the course as well, but we really feel that it is important to look out for these flags, red flags,(...) these situations and then reach out for professional help. Firstly, we do not want any mother to be in pain, so please don't normalise pain with breastfeeding.

(...)

If it is painful, please seek our professional help.(...) The second, you would get a feeling that the baby is not getting optimal milk by a few things. Firstly, the baby is going to be snacky. So, come, drink, go, then not be not dressed for long like just for few minutes, half an hour, 15 minutes, 20 minutes and come again.(...) Then that's possible the baby is not drinking enough. The second would be that you will be able to feel with your own breasts.

(...)

As I said in one of the slides, please do feel your breasts connect with your new body and when you are able to do that, you will also be able to figure out the difference. So for example, when the baby was lashed and drank after the after the feeding was over, you would not really feel that the breasts have gone lighter, you would still feel heavy, you would also be able to see from the baby that the baby is not very calm and relaxed and fussy. This is also a sign that the optimum milk transfer has not happened.(...) Sometimes you also feel that the output in terms of the baby's drinking, be it with their wet diapers. In the initial weeks, we want at least around 6 to 7 full diapers, full wet diapers. If that is not happening or you feel the breasts are not getting lighter or you feel that the baby is quite fussy after the feed and you might also feel that the baby is not coming as much to you as maybe the baby was, that means that the things are not going well. One of the other signs you would feel is that you would feel your supply going down. This is difficult to gauge if you are only breastfeeding, but if you are also pumping, then there is a chance that you would be able to feel that my pumping and my milk coming out is reducing and if you feel any of these triggers including heat around your breast or slightly feeling your breast, slightly clogged, then all of these are alarms, red flags and you would want to reach out for help or professional help. So we would highly encourage during this time you can reach out to us at our Vira website or you can also, you know, to the professionals closer to you, you can reach out to help. But please,(...) doing the right thing is important but also knowing that this is not going right is important. So please keep these things in mind.

(...)

If things are not going well with latching the baby, yes, you might need professional help. But we would like to highlight some common problems with latch which maybe you can correct at home. The firstly is going to connect with the angle of the baby attaching to the nipple, as we said an asymmetric angle, wide open mouth and flanged lips. If you feel that the seal is not proper with their lips, then you can kind of intervene and take your small finger like this and bring their lip out so that they hopefully improve their seal around the nipples. The second is you would notice this is around the sucking of the baby, the rhythmic sucking of the baby. You would notice that they are either doing very shallow, suck and swallow or they are not rhythmic or they are coughing a lot and you know, choking and kind of getting disturbed with the sucking a lot. When this happens, we can do three things. The first thing is unlatch them because there's something with the latch which this could happen even if you have perfectly good latches, you know, nine times out of ten. But there are one or few times when it doesn't happen. When any of this happens, unlatch them, latch them again and now support your breast. As I said in one of the initial breasts, just support your breast either with a C hold or with a U hold and then offer them the breast. Maybe with this, the latch will be better and the nipple will go deeper in their mouth(...) and this way their suck and swallow ratio might improve and also the disorganized rhythm becomes better. This is the first thing to do. Well, the first thing is to unlatch them. The second thing is to latch them with the U or the C hold and the third thing is connect with yourself. Get slightly calmer, you know, relax yourself and breathe. I will cover the breathing part also under the myths and the demit section, but please breathe because whenever we are doing something very important, it's very common that we shallow breathe.

(...)

Breathe nicely as you would breathe nicely, the milk will flow nicely.

(...)

The last three points connect with a sleepy baby or a sleepy mother, a medicated mother or slightly overstimulated mother or child. In these situations, of course, if you can, then please connect again and latch again when the baby is less sleepy and you yourself are also rested. During this time, you might have to use one of the feeds, you might have to do bottled feed in one of the feeds, but if you are able to take that help if needed and come back with the latch, you might notice that the sleepy and the drowsy state was what was interfering with the latch. The second is medication. Sometimes we are on some medications depending on the surgery and procedure.(...) Mostly you would have your medical practitioner helping you with this, but you can always connect with them and raise a concern if you feel that any of the medications is interfering.

(...)

And lastly, overstimulation. This is a point for the family, not just for the mother. For the family around, they can do a huge, huge task, which is of helping the mother stay calm, not overstimulating the atmosphere, not overdoing things around them, just keeping them calm and tidy so that the mother and the baby can connect together and start their breastfeeding or continue the breastfeeding journey.

(...)

With this, we are moving towards the last module, which is breastfeeding myths busted.(...) This entire course is very close to my heart. As I said at the beginning, I am a mother and I've experienced this myself and I work very closely with infants, very closely with women, with mothers. So of course, I really feel that a preparatory knowledge is key when you're starting your breastfeeding journey and sometimes or most of the times we lack that as a family. So I'm in love with the entire course, but this module is my favorite module because there are so many myths around us. Be it you're a mother in Europe, you're a mother in America, South America and Africa in India, in other parts of Asia, you must have heard some of the myths. So as a professional, I will deal with them.(...) Starting with the first and the classic. It's usual for breastfeeding to hurt. That's how you become a good mother. Sore nipples are inevitable.

(...)

Incorrect.(...) New mothers often encounter breastfeeding discomfort initially, but proper positioning and ensuring correct attachment of the baby can prevent sore nipples. Seeking support from a lactation consultant or a skilled professional can aid in overcoming breastfeeding challenges like nipple soreness. Please do not normalize breastfeeding pain. Breastfeeding should not be painful. Seek out for help and don't connect pain as some trophy of being a mother. You don't become a better mother or a good mother or a perfect mother when you are in pain. So please don't keep yourself in pain.

(...)

The second.

(...)

You should wash your nipples before breastfeeding. We did go through this slide where I said do not wipe your nipples or wash or take a bath before the first latch, before the first feeding. But this applies to all the feedings. There is no need to wash your nipples before breastfeeding. You can of course take a bath depending on your day. But you do not need to be washing your nipples before every breastfeeding session.

(...)

Babies are born familiar with their mother's scent and sound. The nipples produce a substance containing the good bacteria that aids the baby's immune system in terms of building it strong and healthy. And it also offers them a similar fragrance as the amniotic fluid which is home for them, which was home for them. So you do not need to wipe your nipples before every breastfeeding session.

(...)

You should separate a newborn and a mother to let the mother rest.(...) This could not be any more wrong. This is so wrong. Please don't do this. Of course as a new mother get your rest. But you or your newborn do not need to be separate for this. Healthcare professionals including us, we fully, fully promote skin to skin or gangroo mother care. This involves placing the baby directly on the mother's skin, bare chest,(...) facilitating breastfeeding initiation, facilitating a lot of attachment and a lot of love.(...) And this starting this practice, especially within the first hour is said to be one of the core milestones to achieve for continuous, regular and successful breastfeeding session.(...) Please also keep in mind that we want the mother to be healing in their postpartum journey, to be healing from the wounds sometimes the internally develop. All of that healing is connected with the baby. When the baby comes close to the mother, mother starts to heal and baby starts to grow. Please remember this mantra and do not separate it. Separate a newborn from the mother. Moving on with our myths. You won't be able to breastfeed unless you do it straight away. This is quite a classic one. This myth can cause unnecessary stress.(...) Please do not let this bother you. While early initiation is ideal, we've discussed the first hour, we've discussed colstrum, we've discussed the golden opportunity. However, that is not the only opportunity. Breastfeeding is a learned skill for both mother and the baby, requiring practice and support. Please seek professional help from the consultants out there, from our super specialist out there. And with patience and support, successful breastfeeding can be achieved even later on, even if it is not started immediately afterwards. So please do not take this pressure. And most importantly, don't think that, oh, I had a C-section, that's why I couldn't breastfeed. Oh, I've had a C-section, so I can't now breastfeed. It's not going to work. Or for some reason my baby was, you know, away from me. Or for some reason my milk came late. Whatever might have happened. Please don't connect this as the ultimate fate of how your breastfeeding is going to be like.(...) These notions and these myths just bring stress. So just disconnect yourself from them.

(...)

The second one, many mothers can't produce enough milk. I have not heard this enough. It's just so much out there. This milk, her milk is not enough. Oh my God, the baby is too small. Oh my God, she is so small. The baby is small. That's why I'm a victim of it myself. I've heard this a lot. Oh, you are tiny. So the baby is tiny. The milk is not enough.

(...)

There are instances that it can happen the milk is not produced or is not produced enough. But let the professional and the mother's body together decide this and guide you. Don't let the myth sit in your head.(...) Listen to the answer very carefully. Most mothers naturally produce sufficient milks for their babies.(...) Factors influencing breast milk production include the babies latch onto the breast,

(...)

the feeding frequency and the effectiveness of milk removal during each feeding.

(...)

Fasting requires support,(...) emphasizing the importance of ongoing guidance from healthcare providers, assistance at home and maintaining good health through proper nutrition and hydration.

(...)

These are the factors we need to keep in mind and not the myth that because someone is small, then the baby is small because the baby is crying and the milk is not enough. Don't connect these random thoughts with your milk not being enough. Keep in mind that you want the baby to be lashed correctly. You want the feeding frequency to be established. You want effective removal of milk from the breast. It's the demand and supply concept. As the milk is effectively removed from the breast, similarly, the milk will be produced enough for the baby. Baby and mother are meant for each other. That's how they come together.

(...)

Moving on to the last myth on this page, you can never use formula if you want to breastfeed.

(...)

This might opt to supplement breastfeeding with formula on certain occasions. This could be a lifestyle thing. This could be a medical thing. This could be a choice. This could also be things like work. This could also be sometimes we are too tired. In any of these, it's crucial to keep in mind that yes, breast milk is the ideal liquid, the ideal liquid gold we want for the baby, but there are safe alternative in terms of baby formulas available. With the help of a skilled professional, with the help of your team, with the help of your family, you can continue to do breastfeeding or formula feeding.

(...)

You can also switch between the two. They are not exhaustive of each other. It can't be that you're breastfeeding, so you can't do formula. Because you've started formula, you can't move to breastfeed. Please keep these points in mind. Moving on with our myths.(...) It's hard to wean a baby if you breastfeed them for more than a year. This is incorrect. There is no evidence suggesting that dispute containing breastfeeding after one year is more challenging. However, research supports the benefits of breastfeeding for up to two years for both mothers and children. Since every mother and baby is unique, they should collectively decide the duration of breastfeeding that suits them and not let any of this myth or any of these concern influence your decision.

(...)

The other myth is very common and is something I also have a special slide about elaborating on which is the next slide. What is the myth? You should only eat plain food or bland food while breastfeeding. This is completely false.(...) Similar to everyone else, breastfeeding mothers should maintain a healthy balanced diet, so you should be eating nutritious foods. Typically, there's no requirement to alter eating habits.(...) These are already exposed to their mother's food choices while they were in the womb. If a mother notices any adverse reactions in her baby or maybe to her to certain foods, then you can please seek out for professional help and guidance and based on the recommendation and based on how you feel, proceed.

(...)

On this note, I would like to share some information with you.

(...)

Breast milk. How do you think breast milk is formed in mother's body? Is it formed in mother's stomach? Is it formed somewhere else?

(...)

Breast milk is formed out of mother's blood.(...) That makes it even more precious. Breast milk is not formed in the stomach of the mother.(...) This means that it's not that we're going to eat a sandwich and that's directly going to get translated to milk. If we eat, you know, meat or chicken, directly translated to milk. If we eat lentils, directly translated to milk. No, it doesn't work like that. Yes, whatever we eat, the nutrients of that are absorbed in the body and in our blood and that nutrition does get transferred to the breast milk. However, breast milk is not made in the stomach of the mother. It is made out of her blood. So with that note in mind,(...) answer, you know, ask yourself, what do I need to eat to keep my blood healthy? To keep our blood healthy, we need to have a nutritious diet. We don't need to have a limited or restricted diet. In fact, if anything, when we restrict too much a new mother in terms of their diet, in terms of their surroundings, we actually make it difficult for them to adapt to this change. This information, especially for the fathers listening to this course, for the family listening to this course, we don't want to make mother's life even more difficult by making it restrictive.(...) This is a big change for them, for their body, for, you know, psychologically, hormonally, emotionally. We don't want to make it any tough by adding layers of restriction. Offer them nutritious food.(...) Offer them nutritious food, take care of them. That's why I use the word offer. She might not be able to make food for her own self. So yes, family can support by making nutritious food for her, but please don't make it limited or restrictive.

(...)

Moving on to the last slide of this module and of course,(...) mother's nutrition. As I said in my last slide, we do not need to give restricted or limited diet to mother.(...) Mother's breast milk is made out of mother's blood. So we want her blood to be nutritious, to be nourished. And for that, the first thing to keep in mind is that we follow a nutritious diet, which includes a mix of all the macro proteins, all the carbohydrates and all the fats and all the other micronutrients.(...) And in this journey, you as a new mother will notice that your hunger drive and your want to eat more has increased. These are the hunger cues which you should follow. New mother needs average approximately 300 to 500 calories. We don't need to calorie count our food, but I just want to leave some ballpark points with you.(...) The first is, as an adult, we eat anywhere between 1600 to 2000 calories. This would mostly include three nice meals, which are a mix of proteins, carbohydrates and fats. And it's going to include two snacks. While we are eating that, a mother's need is to have an increased 300 to 500 calories. This could be eating more protein. This could be eating another pair of snacks. This could be having, you know, a little bit, little bit few munches around their breastfeeding. While they are eating this and they are adding these calories, this intake is not just limited to breast milk. It's not that all these calories are going to go into breast milk. This is something she needs for herself.(...) So please keep in mind that we're looking at an extra intake of 300 to 500 calories. In this journey, we are looking at around 15 to 20 grams of protein in these calories. And while you're doing your breastfeeding journey, you would have this want to eat more. You would have this urge to eat more. So please follow your hunger cues.

(...)

As I said, all of this is not just for breast milk. It is important for you to heal. There's extensive tissue healing which needs to be done after birth, be it having a vaginal birth or having a C-section. The tissues need to heal and for that we need to eat healthy and nutritious food. In these phases and during these breastfeeding sessions, you would feel that you would want to stay hydrated. So please stay consistent with your fluid intake. You don't need to drink more than you're thirsty, but there's a strong chance that when your breastfeeding you will feel thirsty. So stay hydrated, eat proteins, more proteins if you can, eat approximately 300 to 500 calories more. And how to achieve this? Simply follow your hunger cues.

(...)

And the last point I want to say, care, support and lots of understanding. This is part of nutrition. This is not maybe the food which the mother is eating, but this is the food which the mother's body needs. So please give them care, a lot of support and a lot of understanding.(...) And then let the baby and the mother start their breastfeeding journey. And if they need any help, please seek out for professional help.

(Music)

(...)

With this, we will wrap our course breastfeeding first steps. We really hope that it has been useful for you. It will prepare you, and we would look forward to having you in our live session. Before we end the course, I would like to leave some takeaways with you. The first is communication.

(...)

There are a lot of stuffs I said in this course, like first milk, skin to skin, wanting the baby to be next to you, which are good to upfront communicate with your spice, with your family, or with your guy neck. If you communicate these things with your institution, with the people around you, you will be able to share your wishes with them. You can upfront tell them that you would want the first milk colstrom to be given to your baby. You could tell them that you would want to perform skin to skin whenever you and the baby get together.

(...)

If you have a natural birth or vaginal birth or normal birth, as we call it, chances are that the baby will be given to you straight away and you will be able to perform skin to skin. If you have a cesarean c-section, there might be some distance between you and the baby. If you have done the upfront communication, which is the point I mentioned above,(...) with your guy neck and your family, then once you are recovering and the baby comes into the room, they will be able to give the baby to you so that you can start your first hour post delivery activities.(...) First hour, also known as ideally the golden hour, is the perfect time for the baby to come to you. However, if for some reason you miss this first hour, do not panic. Perform your first hour activities whenever baby and you get together, be it in the third hour or the fourth or the sixth hour, but whenever you both get together, perform your first hour activities.

(...)

Breastfeeding is not meant to be painful. Please seek out professional help if it is painful for you. Breastfeeding follows a demand and supply theory. The more milk comes out of the breast, the more milk is extracted out of the breast, the more the body gets signal to produce. So please follow your feeding frequencies, latch the baby often. And in this journey, if you are struggling at all, then pumping can be your savior. Pumping is quite a boon. And in this setup, if you're not able to follow a rhythm, you can ask your professional who you're working with for some guidance on pumping. And maybe it will be a savior in your journey and help you maintain your milk supply.

(...)

We thank you so much for being part of our course. Hope all of this information was useful for you, especially around the first hour, cold, strong skin to skin and more. Please keep these takeaways with you. And we look forward to having you in our live session, where we will do the workshop with our basics in positioning, basic and different latch positions. So please do come into the live workshop with a small pillow, which you can use as a dummy. Thank you so much for joining us. We stay in touch and you can follow us for more of our courses.

"""


# Generation Configuration
generation_config = GenerationConfig(
    temperature=0.7, # Balanced temperature for natural but focused responses
    top_p=0.9, # Slightly more focused for better structure
    top_k=40, # More focused vocabulary for professional health advice
    max_output_tokens=8192, # Max output for Gemini Flash (adjust if using a different model with different limits)
)

# Safety Settings
safety_settings = [
    {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
]

# Store active models per session_id (less critical now, but good for consistency if we add state later)
# Key: session_id (string), Value: genai.GenerativeModel object
active_models = {}

def get_model_for_session(session_id: str):
    """Gets or creates a model instance for the session."""
    if session_id not in active_models:
        logger.info(f"Creating new model instance for session: {session_id}")
        try:
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                safety_settings=safety_settings,
                generation_config=generation_config,
                system_instruction=SYSTEM_PROMPT
            )
            active_models[session_id] = model
            return model
        except Exception as e:
            logger.error(f"Error initializing model for session {session_id}: {e}")
            raise
    return active_models[session_id]

def generate_answer_for_question(session_id: str, selected_question_text: str, language: str = "en"):
    """
    Generates an answer for a pre-selected question using the full transcript in the system prompt,
    tailored to the specified language.
    """
    model = get_model_for_session(session_id)

    language_map = {
        "en": "English",
        "hi": "Hindi",
        "bn": "Bengali",
        "mr": "Marathi",
        "kn": "Kannada",
        "gu": "Gujarati"
    }
    target_language_name = language_map.get(language, "English") # Default to English if code is unknown

    # Modify the prompt to include language instruction
    prompt_for_selected_question = (
        f"A new mother is asking the following question (originally in English): \"{selected_question_text}\"\n\n"
        f"Please provide a comprehensive, well-structured answer with practical guidance, **strictly in {target_language_name}**.
"
        f"Ensure your entire response, including any headings or bullet points, is in {target_language_name}. "
        f"Follow all other guidelines from the system prompt regarding tone, style, and content based on the Knowledge Base."
    )

    try:
        logger.info(f"Generating answer for session {session_id}, language: {target_language_name}, question: '{selected_question_text[:100]}...'")
        # For a direct Q&A based on a massive system prompt, generate_content is more direct
        # than start_chat().
        response = model.generate_content(prompt_for_selected_question)
        logger.info(f"Received response for session {session_id}")

        if not response.parts:
            logger.warning(f"Response potentially blocked for session {session_id}. Prompt feedback: {response.prompt_feedback}")
            block_reason_message = ""
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                 block_reason_message = f" (Reason: {response.prompt_feedback.block_reason.name})"

            # Check candidates for safety ratings if parts are empty
            candidate_safety_issues = []
            if response.candidates:
                for cand in response.candidates:
                    if cand.safety_ratings:
                        for rating in cand.safety_ratings:
                            if rating.probability.value > 2: # THRESHOLD_UNSPECIFIED=0, NEGLIGIBLE=1, LOW=2, MEDIUM=3, HIGH=4
                                candidate_safety_issues.append(f"{rating.category.name} ({rating.probability.name})")
            if candidate_safety_issues:
                block_reason_message += f" Content issues: {', '.join(candidate_safety_issues)}."

            return f"My apologies, but I cannot provide a detailed answer to that right now due to content guidelines{block_reason_message}. Please try rephrasing or selecting a different question."

        response_text = "".join(part.text for part in response.parts)
        return response_text

    except Exception as e:
        logger.error(f"Error during generate_answer_for_question for session {session_id}: {e}")
        return f"Sorry, I encountered an error trying to generate an answer: {str(e)}"

# Renaming for clarity in the new flow
send_message = generate_answer_for_question

# This function is less critical now as we don't maintain a long chat history for this flow,
# but keeping the structure for potential future use or if session-specific model instances are beneficial.
def start_new_chat(session_id: str):
    """Ensures a model instance is ready for the session."""
    logger.info(f"Ensuring model is ready for session: {session_id}")
    get_model_for_session(session_id) # This will create if not exists
    return True # Indicate success or readiness