from gpt4all import GPT4All
from datetime import datetime

model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", device='gpu') # device='amd', device='intel'

class Session:
    '''A session of GPT-4-All. It manages the history of the conversation and the generator. DO NOT USE THIS CLASS DIRECTLY. Use GPTManager instead.'''
    last_active: datetime

    def __init__(self, sys_prompt, prompt_template):
        self.isActive = True
        self.template = prompt_template
        self.history = [{"role": "system", "content": sys_prompt}]
        self.generator = self.sessionMan()
        self.last_active = datetime.now()

    def sessionMan(self):
        '''A generator function that manages the conversation and history. It yields the responses.'''
        while self.isActive:
            model._history = self.history
            model._current_prompt_template = self.template

            response = model.generate(self._prompt, max_tokens=1000)

            self.history.append({"role": "user", "content": self._prompt})
            self.history.append({"role": "system", "content": response})
            yield response

    def prompt(self, prompt):
        '''Ask something to the model. Returns the response.'''

        self.last_active = datetime.now()
        self._prompt = prompt
        return next(self.generator)
    
    def close(self):
        '''Closes the session and deletes the generator.'''

        self.isActive = False
        del self.history
        self.generator.close()


sessions: dict[str, Session] = {}

class GPTManager:
    '''Manages the GPT sessions. All prompts should be done through this class.'''
    def __init__(self):
        pass

    def create_session(self, sessionID: str, sys_prompt: str, prompt_template: str) -> None:
        '''
        Creates a new session. The sessionID must be unique or it will overwrite the previous session.
        
        :param sessionID: The unique identifier of the session. Must be unique. 
        :type sessionID: str
        :param sys_prompt: The system prompt for the session. It is the first step in the conversation and will give it context.
        :type sys_prompt: str
        :param prompt_template: The template for the prompts in the session. Will get used in every prompt and will add the prompt where {0} is present.
        :type prompt_template: str
        '''
        if sessionID in sessions:
            self.delete_session(sessionID)

        sessions[sessionID] = Session(sys_prompt, prompt_template)

    def delete_session(self, sessionID: str) -> None:
        """
        Deletes a session. If a DB is implemented, the session remains in the database.
        
        :param sessionID: The unique identifier of the session to be deleted.
        :type sessionID: str
        """

        # TODO add a backup to a database

        sessions[sessionID].close()
        del sessions[sessionID]

    def get_session(self, sessionID: str) -> Session:
        """
        Returns the session object. Use this to manage the session directly.
        
        :param sessionID: The unique identifier of the session to be retrieved.
        :type sessionID: str
        :return: The session object.
        """

        return sessions[sessionID]
    
    def prompt(self, sessionID: str, prompt: str) -> str:
        """
        Prompts the model with a session. Returns the response. Use this to call any prompts
        
        :param sessionID: The unique identifier of the session to be prompted.
        :type sessionID: str
        :param prompt: The prompt to be sent to the model.
        :type prompt: str
        :return: The response from the model.
        """

        if sessionID not in sessions:
            raise ValueError(f"Session {sessionID} does not exist")

        return sessions[sessionID].prompt(prompt)
    
    def close(self):
        # TODO: maybe add backups to database?
        for session in sessions.values():
            session.close()
    

# tests
if __name__ == "__main__":
    manager = GPTManager()

    manager.create_session("test", """You are a personal trainer. 
                           The person you are training works on a front-desk call center and needs a lot of help while talking to costumers. 
                           You must give your trainee a list of recommendations, in a positive leadership manner. 
                           You are talking directly to your trainee, make sure to make it as personal as possible. 
                           Note that the average call duration is 3 minutes, it should be under that.
                           A negative sentiment means that they might have been angry, stressed, or without a positive attitude.
                           Durations are given in milliseconds.
                           Make sure the Agent NEVER interrupts the customer.
                           Talk time should be as little as possible.
                           Your trainee's name is unknown, however, refer to it in second person, avoid saying things like 'the agent'. Try to start feedback like: 'You should...' or 'Have you tried ...'""", 
                           "### Call record:\n{0}\n\n### What can I (the agent) improve based on the last call record? Please give me feedback on what I can improve!\n")

    print(manager.prompt("test", """AGENT: (NEUTRAL)Er.
CUSTOMER: (NEUTRAL)Hello.
AGENT: (POSITIVE)Hello, sir. My name is Pablo Cruz. And I'm glad to help you. Please. Can you tell? Can you tell us your problem?
CUSTOMER: (NEUTRAL)Yes. Hello. Hello. Um, I'm talking to you because I am making my refund for the Um You know, Recently there was a new concert.
CUSTOMER: (NEUTRAL)Uh, but he got the the the Kobe So or influenza? I believe.
CUSTOMER: (NEGATIVE)Um, I'm here. I'm calling to get a refund on my ticket because the concerts did not happen. The event was cancelled, so I want my My my refund.
AGENT: (NEUTRAL)Gail, Let me check. Do you know? When was the date of your Concert.
CUSTOMER: (NEUTRAL)Yeah. Yes, I believe it was yesterday.
AGENT: (NEUTRAL)Okay? Let me search Yes, indeed, sir. Your concert was cancelled. But
AGENT: (NEGATIVE)Uh, that's unfortunately we can refund you. Because it was And some of the policies of the Um, manager of your artist, so We can
AGENT: (NEUTRAL)Er, do anything about your case.
CUSTOMER: (NEGATIVE)So you're telling me you're Basically scamming right about
CUSTOMER: (NEUTRAL)Cycle grid. People that wanted to go to the 5000 people that are, we're going to the concert.
AGENT: (NEUTRAL)Er, no, sir. The the the The case was that Am I know you're, uh I realized Um
AGENT: (NEUTRAL)Uh, A type of Relation and Ticketmaster we can do Anything about our customers. Er. So is
AGENT: (NEUTRAL)In Not on our hands. Basically
CUSTOMER: (NEUTRAL)But I believe she published on Twitter. The They are going to do something about that, right?
AGENT: (NEGATIVE)No, sir.
CUSTOMER: (POSITIVE)I believe he could. Master has a refund policy. Right?
AGENT: (MIXED)Jess, but yes, but only works. In our
CUSTOMER: (POSITIVE)And the exchanges as well.
AGENT: (NEGATIVE)Yes, but it only works, eh? Those refunds only works. When Ticketmaster Is it main? Eh? The main person that organizes the concert.
AGENT: (NEUTRAL)And your contract was er Um, established by another. Uh, company so we can do anything about your refunds.
CUSTOMER: (NEUTRAL)Hmm. Mhm. Okay, I'm gonna Um Make another call in about an hour.
CUSTOMER: (NEGATIVE)Basically asking the same, but I'm gonna see if I can refund it anyway.
AGENT: (NEUTRAL)Okay, sir.
CUSTOMER: (NEUTRAL)If not, I want to talk to your manager.
AGENT: (POSITIVE)I agree there.
CUSTOMER: (NEUTRAL)See you then.
END OF CHAT

Chat Duration: 195795
Interruptions: 1
No talk time: 4922
Agent sentiment: -0.4
Customer sentiment: 0
"""))
    
    manager.delete_session("test")
