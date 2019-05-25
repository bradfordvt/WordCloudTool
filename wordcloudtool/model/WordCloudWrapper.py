"""
@package wordcloudtool.model
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 25, 2019 - Initial release
Specialized class for managing a WordCloud instance.
"""
import multidict as multidict
import operator
import numpy as np
import cv2
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloudtool.model.StopWords import StopWords


class WordCloudWrapper(object):
    """
    A specialized class for managing the creation and generation of a WordCloud.
    """
    inst = None
    lock = True

    @staticmethod
    def get_WordCloudWrapper():
        """
        Factory method for creating a single use instance (Singleton) of the control.
        :return:
        """
        if WordCloudWrapper.inst is None:
            WordCloudWrapper.lock = False  # workaround to create private constructor enforcement
            WordCloudWrapper.inst = WordCloudWrapper()
        return WordCloudWrapper.inst

    def __init__(self):
        """
        Constructor
        """
        self.image_observers = []
        self.frequency_observers = []
        self.stopwords = StopWords()
        self.wordcloud_image = None
        self.freq_image = None
        self.freq_size = 20
        self.wordcloud = WordCloud(width=800, height=800,
                                   background_color='white',
                                   stopwords=set(self.stopwords.get_stopwords()),
                                   min_font_size=10)

    def get_width(self):
        return self.wordcloud.width

    def set_width(self, width):
        self.wordcloud.width = width

    def get_heigth(self):
        return self.wordcloud.height

    def set_heigth(self, heigth):
        self.wordcloud.height = heigth

    def get_background_color(self):
        return self.wordcloud.background_color

    def set_background_color(self, background_color):
        self.wordcloud.background_color = background_color

    def get_stopwords(self):
        return self.stopwords

    def set_stopwords(self, stopwords):
        if isinstance(stopwords, StopWords):
            self.stopwords = stopwords
        else:
            raise ValueError('stopwords is not a StopWords object.')

    def get_min_font_size(self):
        return self.wordcloud.min_font_size

    def set_min_font_size(self, min_font_size):
        self.wordcloud.min_font_size = min_font_size

    def get_freq_size(self):
        return self.freq_size

    def set_freq_size(self, size):
        self.freq_size = size

    def generate_from_count(self, count):
        """
        Generate the cloud image from a dictionary of word and counts.
        :param count: A dictionary in the form {word: count}
        :return:
        """
        stopwords = set([i.lower() for i in self.stopwords.get_stopwords()])
        # remove stopwords
        count = {x: count[x] for x in count if x.lower() not in stopwords}
        # Need to normalize the frequencies
        full_terms_dict = multidict.MultiDict()
        for key in count:
            full_terms_dict.add(key, count[key])
        self.wordcloud.generate_from_frequencies(full_terms_dict).to_file('wordcloud.png')
        # self.wordcloud_image = self.wordcloud.generate_from_frequencies(full_terms_dict).to_image()
        self.wordcloud_image = cv2.imread('wordcloud.png')
        sorted_x = sorted(count.items(), key=lambda cnt: cnt[1], reverse=True)
        plot_words = [x[0] for x in sorted_x[:self.freq_size]]
        plot_counts = [x[1] for x in sorted_x[:self.freq_size]]
        # Plot histogram using matplotlib bar().
        indexes = np.arange(len(plot_words))
        fig = plt.bar(indexes, plot_counts)
        plt.xticks(indexes, plot_words, rotation=90)
        plt.savefig('histogram.png')
        # plt.close(fig)
        plt.close()
        self.freq_image = cv2.imread('histogram.png')
        self.__notify_image_observers()
        self.__notify_frequency_observers()

    def get_cloud_image(self):
        """
        Returns the generated image of the cloud.
        :return:
        """
        return self.wordcloud_image

    def get_frequency_image(self):
        """
        Returns the generated image of the frequency plot of the top 20 words.
        :return:
        """
        return self.freq_image

    def register_image_observer(self, observer):
        """
        Register an image client that needs to be notified when the words for the cloud has been updated.
        :param observer: Client method to be called when list has been updated.
        :return:
        """
        self.image_observers.append(observer)

    def unregister_image_observer(self, observer):
        """
        Unregister an image client so it will no longer be notified of changes.
        :param observer: Client method to be removed from the list of observers.
        :return:
        """
        self.image_observers.remove(observer)

    def register_frequency_observer(self, observer):
        """
        Register an frequency client that needs to be notified when the words for the cloud has been updated.
        :param observer: Client method to be called when list has been updated.
        :return:
        """
        self.frequency_observers.append(observer)

    def unregister_frequency_observer(self, observer):
        """
        Unregister an frequency client so it will no longer be notified of changes.
        :param observer: Client method to be removed from the list of observers.
        :return:
        """
        self.frequency_observers.remove(observer)

    def __notify_image_observers(self):
        """
        Utility to notify image observers of a change to the words in the cloud.
        Observers must have the signature where this instance is passed as the only argument.
        Example:
        CloudView.cloud_observer(cloud)
        :return:
        """
        for observer in self.image_observers:
            observer(self)

    def __notify_frequency_observers(self):
        """
        Utility to notify frequency observers of a change to the words in the cloud.
        Observers must have the signature where this instance is passed as the only argument.
        Example:
        CloudView.cloud_observer(cloud)
        :return:
        """
        for observer in self.frequency_observers:
            observer(self)


