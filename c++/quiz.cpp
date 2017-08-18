#include <cctype>
#include <cstdio>
#include <iostream>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <vector>

#include "random_selector.h"
#include "rare_mode.h"

using namespace std;    

class NoQuestionsLoaded {};


class QuizModel
{
public:
    QuizModel() : correct(0), not_correct(0), current_element_idx(0) {}
    
    void add_sentence(const string& question, const string& answer);

    void mark_correct() { correct += 1; }
    void mark_incorrect() { not_correct += 1; }

    int get_correct() const { return correct; }
    int get_incorrect() const { return not_correct; }
    int get_total() const { return quiz_data.size(); }

    void select_random_question();
    const string& get_question() const;
    const string& get_answer() const;

    typedef pair<string, string> quiz_pair;
    
private:
    int correct, not_correct;
    vector<quiz_pair> quiz_data;

    util::RandomSelector<> selector;
    int current_element_idx;
};

void QuizModel::add_sentence(const string& question, const string& answer)
{
    quiz_data.push_back(quiz_pair(question, answer));
}

void QuizModel::select_random_question() 
{
    if (quiz_data.size() > 0)
        current_element_idx = \
            selector.select_idx(quiz_data.begin(), quiz_data.end());
}

const string& QuizModel::get_question() const
{
    if (get_total() == 0) {
        throw NoQuestionsLoaded();
    }
    return quiz_data[current_element_idx].first;
}

const string& QuizModel::get_answer() const
{
    if (get_total() == 0) {
        throw NoQuestionsLoaded();
    }
    return quiz_data[current_element_idx].second;
}


class KeyStroke 
{
public:
    virtual ~KeyStroke() {}
    virtual void handle() const = 0;

    const string& get_help() const { return help; }
    
protected:
    string help;
};
    

class ModelKeyStroke : public KeyStroke
{
public:
    ModelKeyStroke(QuizModel& model) : model_ref(model) {} 

protected:
    QuizModel& model_ref;
};


class NextQuestion : public ModelKeyStroke
{
public:
    NextQuestion(QuizModel& model) : ModelKeyStroke(model) {
        help = "Show the next question.";
    }
    
    void handle() const 
    {
        model_ref.select_random_question();
        cout << model_ref.get_question() << endl;
    }
};


class Scores : public ModelKeyStroke 
{
public:
    Scores(QuizModel& model) : ModelKeyStroke(model) {
        help = "Display the score so far.";
    }

    void handle() const
    {
        cout << "Scored " << model_ref.get_correct() << " correct answers and "
             << model_ref.get_incorrect() << " incorrect ones." << endl;
    }
};   


class Answer : public ModelKeyStroke
{
public:
    Answer(QuizModel& model) : ModelKeyStroke(model) {
        help = "Display the answer for the current question.";
    }

    void handle() const
    {
        cout << model_ref.get_answer() << endl;
    }
};

class MarkAnswer : public ModelKeyStroke
{
public:
    MarkAnswer(QuizModel& model, bool correct) :
        ModelKeyStroke(model), correct(correct) {
        if (correct) 
            help = "Mark answer as correct.";
        else
            help = "Mark answer as incorrect.";
    }
    
    void handle() const
    {
        if (correct) {
            model_ref.mark_correct();
            cout << "Answer marked as correct." << endl;
        } else {
            model_ref.mark_incorrect();
            cout << "Answer marked as incorrect." << endl;
        }    
    }
private:
    bool correct;
};


class RareMode
{
public:
    RareMode(bool echo=true) : started(false), echo(echo) {}
    ~RareMode() {stop();}
    void start();
    void stop();
    char read() const;
private:
    bool started;
    bool echo;
    
    struct termios* p_old;
};

void RareMode::start()
{
    if (!started) {
        p_old = rare_mode_start(echo);
        started = true;
    }
}

void RareMode::stop()
{
    if (started) {
        rare_mode_stop(p_old);
        started = false;
    }
}

char RareMode::read() const 
{
    return rare_mode_read_one();
}


class KeyStrokeDispatcher 
{
public:
    void loop_forever() const;
    void dispatch_one(char ch) const;
    void handle_invalid(char ch) const;

    void register_key(char key, unique_ptr<KeyStroke> keystroke);

    typedef map<char, unique_ptr<KeyStroke> > keystroke_map;
    const keystroke_map& get_keystrokes() const { return keystrokes; }
    
private:
    keystroke_map keystrokes;
};

void KeyStrokeDispatcher::loop_forever() const
{
    RareMode rm(false);
    rm.start();
    while (true) {
        char ch = rm.read();
        dispatch_one(ch);
    }
    rm.stop();
}

void KeyStrokeDispatcher::dispatch_one(char ch) const 
{
    auto it = keystrokes.find(ch);
    if (it == keystrokes.end()) {
        handle_invalid(ch);
    } else {
        it->second->handle();
    } 
}

void KeyStrokeDispatcher::handle_invalid(char ch) const
{
    stringstream out;
    if (isprint(ch)) {
        out << "'" << ch << "'";
    } else {
        out << "<unprintable> (hex " << std::hex << (int)ch << ")";
    }
    cerr << "Invalid keystroke: " << out.str() << endl;
}

void KeyStrokeDispatcher::register_key(
    char key, unique_ptr<KeyStroke> keystroke)
{
    keystrokes[key] = move(keystroke);
}

class Help : public KeyStroke
{
public:
    Help(KeyStrokeDispatcher& dispatcher) : dispatcher(dispatcher) {
        help = "Show help for available commands.";
    }

    void handle() const 
    {
        cout << "Available keystrokes:" << endl;
        for (auto const& iter : dispatcher.get_keystrokes()) {
            cout << iter.first << " : " << iter.second->get_help() << endl;
        }
    }
    
private:
    KeyStrokeDispatcher &dispatcher;
};



int main() {
    KeyStrokeDispatcher dispatcher;

    QuizModel quiz_model;
    quiz_model.add_sentence("foo bar", "foo bar answer");
    quiz_model.add_sentence("foo bar 2", "foo bar 2 answer");
    quiz_model.add_sentence("foo bar 3", "foo bar 3 answer");
    
    dispatcher.register_key(
        'n', unique_ptr<KeyStroke>(new NextQuestion(quiz_model)));
    dispatcher.register_key(
        's', unique_ptr<KeyStroke>(new Scores(quiz_model)));
    dispatcher.register_key(
        'a', unique_ptr<KeyStroke>(new Answer(quiz_model)));
    dispatcher.register_key(
        'c', unique_ptr<KeyStroke>(new MarkAnswer(quiz_model, true)));
    dispatcher.register_key(
        'i', unique_ptr<KeyStroke>(new MarkAnswer(quiz_model, false)));
    dispatcher.register_key(
        'h', unique_ptr<KeyStroke>(new Help(dispatcher)));

    dispatcher.loop_forever();
        
    return 0;
}
