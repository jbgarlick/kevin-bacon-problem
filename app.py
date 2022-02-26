import networkx as nx
from matplotlib import pyplot as plt
import streamlit as st
import numpy as np

class MovieGraph:
    """Class for solving the Kevin Bacon problem with movie data from IMDb."""

    def __init__(self, filename="movie_data.txt"):
        """Initialize a set for movie titles, a set for actor names, and an
        empty NetworkX Graph, and store them as attributes. Read the speficied
        file line by line, adding the title to the set of movies and the cast
        members to the set of actors. Add an edge to the graph between the
        movie and each cast member.

        Each line of the file represents one movie: the title is listed first,
        then the cast members, with entries separated by a '/' character.
        For example, the line for 'The Dark Knight (2008)' starts with

        The Dark Knight (2008)/Christian Bale/Heath Ledger/Aaron Eckhart/...

        Any '/' characters in movie titles have been replaced with the
        vertical pipe character | (for example, Frost|Nixon (2008)).
        """
        # Initialize the movie set and actor names set, as well as a nx graph object
        self.movie_titles = set()
        self.actor_names = set()
        self.G = nx.Graph()
        # Read the file and save the contents, close the file
        inputfile = open(filename, 'r', encoding='utf-8')
        lines = inputfile.readlines()
        inputfile.close()
        for line in lines:
            # strip and split the lines, so that we have a list for each movie
            movie_list = line.strip().split('/')
            # Pop off the first element (the movie) so that the list becomes just actors
            title = movie_list.pop(0)
            # Add the movie title to the set of movie titles
            self.movie_titles.add(title)
            # Go thorugh each actor in the movie, add them to the set of actors, add an edge between the movie and each actor
            for i in movie_list:
                self.actor_names.add(i)
                self.G.add_edge(title, i)


    def path_to_actor(self, source, target):
        """Compute the shortest path from source to target and the degrees of
        separation between source and target.

        Returns:
            (list): a shortest path from source to target, including endpoints and movies.
            (int): the number of steps from source to target, excluding movies.
        """
        # Create an nx list of the shortest path from source to target
        shortest_path = nx.shortest_path(self.G, source, target)
        # Empty list to store just the actor path
        actor_path = []
        for i in shortest_path:
            # Only store the element of shortest path list that are actors
            if i not in self.movie_titles:
                actor_path.append(i)
        # Return the shortest path from source to target, including endpoints and movies, as well as the number of steps from source to target, excluding movies
        return shortest_path, len(actor_path)-1


    def average_number(self, target):
        """Calculate the shortest path lengths of every actor to the target
        (not including movies). Plot the distribution of path lengths and
        return the average path length.

        Returns:
            (float): the average path length from actor to target.
        """
        # Dictionary of all paths between every actor and target
        all_paths = nx.shortest_path_length(self.G, target=target)
        # Empty list for the lengths of paths
        values = []
        # Go through each key in the dictionary
        for value in all_paths.keys():
            # Only consider the paths to the actors, not the paths to movies
            if all_paths[value] % 2 == 0:
                # Add the length of the path, divided by two in order to just get the actors, not the movies
                values.append(all_paths[value] // 2)
        # Create a histogram of the path lengths between all actors and the target
        # plt.hist(values, bins=[i-.5 for i in range(8)])
        # plt.title('Average path lengths of every actor to ' + str(target))
        # plt.show()
        fig, ax = plt.subplots()
        ax.hist(values, bins=[i-.5 for i in range(8)])
        ax.set_title('Average score of every actor to ' + str(target))
        ax.set_ylabel('Number of Actors')
        ax.set_xlabel('# of Movies Away from Actor')
        # Return the average path length from all actors to the target actor
        return fig, sum(values)/len(values)








st.title('The Kevin Bacon Problem')
st.subheader('A fun way to learn about graph theory.')
st.write('Have you ever heard about the six degrees of Kevin Bacon?')
st.write('Basically, the idea is that every actor in hollywood is typically connected to Kevin Bacon by 6 movies or less.')
st.write('Think of it like this: ')
st.markdown('Kevin Bacon was in _Patriots Day (2016)_')
st.markdown('Mark Falvo was also in _Patriots Day_, and was in _Captain America: Civil War (2016)_')
st.markdown('Tom Holland was in _Captain America: Civil War_.')
st.write('So, Kevin Bacon and Tom Holland are just one actor away from each other, giving Tom Holland a score of 2 (or two degrees of separation)')
st.write('Try it yourself! Click the button below to select randomly or type in two actors\' names and see how they\'re connected.')

obj = MovieGraph('movie_data_small.txt')
actor_list = obj.actor_names
button2 = st.button('Choose random actors')
col1, col2 = st.columns(2)

with col1:
    actor1 = st.text_input('Input the first actor: ')

with col2:
    actor2 = st.text_input('Input another actor: ')

button1 = st.button('Run')
st.write('If an error occurs, make sure the names are spelled correctly.')

if button1:
    if actor1 == '' or actor2 == '':
        st.write('Select two actors.')
    else:
        path, score = obj.path_to_actor(actor1, actor2)
        st.write(path)
        st.write("Score: ", score)
        st.write("Shortly, two graphs will appear showing the distribution of scores for the selected actors.")
        st.write("A score of 1 means that two actors are in the same movie. 2 means that one actor connects them, and so on.")
        col1, col2 = st.columns(2)

        with col1:
            fig, average = obj.average_number(actor1)
            st.pyplot(fig)
            st.text('Average score: ' + str(average))

        with col2:
            fig2, average2 = obj.average_number(actor2)
            st.pyplot(fig2)
            st.text('Average score: ' + str(average2))


if button2:
    actor1 = np.random.choice(list(actor_list), 1)[0]
    actor2 = np.random.choice(list(actor_list), 1)[0]
    path, score = obj.path_to_actor(actor1, actor2)
    st.write('Actors selected: ' + str(actor1) + " & " + str(actor2))
    st.write(path)
    st.write("Score: ", score)
    st.write("Shortly, two graphs will appear showing the distribution of scores for the selected actors.")
    st.write("A score of 1 means that two actors are in the same movie, 2 means that one actor connects them, etc.")
    col1, col2 = st.columns(2)

    with col1:
        fig, average = obj.average_number(actor1)
        st.pyplot(fig)
        st.text('Average score: ' + str(average))

    with col2:
        fig, average = obj.average_number(actor2)
        st.pyplot(fig)
        st.text('Average score: ' + str(average))



