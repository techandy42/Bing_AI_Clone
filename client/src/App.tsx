import React, { useState, useEffect, KeyboardEvent } from 'react'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faSearch,
  faArrowRight,
  faSpinner,
} from '@fortawesome/free-solid-svg-icons'

const App: React.FC = () => {
  const [searchValue, setSearchValue] = useState<string>('')
  const [bgImage, setBgImage] = useState<string>('')
  const [message, setMessage] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [displayedMessage, setDisplayedMessage] = useState<string>('')
  const [footerSearchValue, setFooterSearchValue] = useState<string>('')
  const [footerLoading, setFooterLoading] = useState<boolean>(false)
  const [footerMessage, setFooterMessage] = useState<string>('')
  const [displayedFooterMessage, setDisplayedFooterMessage] =
    useState<string>('')

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchValue(e.target.value)
  }

  const handleFooterSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFooterSearchValue(e.target.value)
  }

  const handleSearch = () => {
    setLoading(true)
    axios
      .post(`${import.meta.env.VITE_SERVER_URL}/search`, { query: searchValue })
      .then((response) => {
        const { message } = response.data
        setMessage(message)
      })
      .catch((error) => {
        console.log('Error performing search', error)
      })
      .finally(() => {
        setLoading(false)
      })
  }

  const handleFooterSearch = () => {
    // Set footer loading state to true
    setFooterLoading(true)

    axios
      .post(`${import.meta.env.VITE_SERVER_URL}/chat`, {
        search_chatbot_result: message,
        user_input: footerSearchValue,
      })
      .then((response) => {
        const { message } = response.data
        setFooterMessage(message)
      })
      .catch((error) => {
        console.log('Error performing search in footer', error)
      })
      .finally(() => {
        // Reset footer loading state to false
        setFooterLoading(false)
      })
  }

  useEffect(() => {
    let index = 0
    const words = message ? message.split(' ') : []
    let tempMessage = ''

    const interval = setInterval(() => {
      if (index < words.length) {
        tempMessage = `${tempMessage} ${words[index]}`
        setDisplayedMessage(tempMessage.trim())
        index++
      } else {
        clearInterval(interval)
      }
    }, 50)

    return () => {
      clearInterval(interval)
    }
  }, [message])

  useEffect(() => {
    let index = 0
    const words = footerMessage ? footerMessage.split(' ') : []
    let tempMessage = ''

    const interval = setInterval(() => {
      if (index < words.length) {
        tempMessage = `${tempMessage} ${words[index]}`
        setDisplayedFooterMessage(tempMessage.trim())
        index++
      } else {
        clearInterval(interval)
      }
    }, 50)

    return () => {
      clearInterval(interval)
    }
  }, [footerMessage])

  useEffect(() => {
    axios
      .get(
        `https://api.unsplash.com/photos/random?query=nature&client_id=${
          import.meta.env.VITE_UNSPLASH_ACCESS_KEY
        }`,
      )
      .then((response) => {
        setBgImage(response.data.urls.full)
      })
      .catch((error) => {
        console.log('Error fetching image', error)
        setBgImage('/aurora_wallpaper.jpg')
      })
  }, [])

  const replaceUrlsWithLinks = (text: string): string => {
    const urlRegex = /<([^>]+)>/g

    return text.replace(urlRegex, (_, url) => {
      return `<a href="${url}" style="color: blue;" target="_blank">${url}</a>`
    })
  }

  return (
    <div
      className='flex flex-col h-auto min-h-screen bg-cover bg-center bg-repeat-y'
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      <header className='w-full p-4'>
        <div className='container mx-auto flex justify-center'>
          <div className='relative text-gray-600 w-96'>
            <input
              type='search'
              name='search'
              className='bg-white h-12 px-5 pr-10 pl-10 rounded-full text-sm focus:outline-none w-full shadow-md'
              value={searchValue}
              onChange={handleSearchChange}
              onKeyDown={(e: KeyboardEvent<HTMLInputElement>) => {
                if (e.key === 'Enter' && !loading) {
                  handleSearch()
                }
              }}
              placeholder='Search Google with GPT-3.5'
              disabled={loading}
            />
            <button
              type='submit'
              className='absolute right-0 top-0 mt-3 mr-4'
              onClick={handleSearch}
              disabled={loading}
            >
              <FontAwesomeIcon icon={faArrowRight} className='text-gray-600' />
            </button>
            <div className='absolute left-0 top-0 mt-3 ml-4'>
              <FontAwesomeIcon icon={faSearch} className='text-gray-600' />
            </div>
          </div>
        </div>
        {loading && (
          <div className='text-center mt-2'>
            <FontAwesomeIcon
              icon={faSpinner}
              size='2x'
              className='text-blue-500 animate-spin'
            />
          </div>
        )}
      </header>
      <main className='flex-grow p-4'>
        {displayedMessage.trim() && (
          <div className='bg-white p-4 rounded-lg shadow-md mx-4 max-h-[1200px] overflow-y-auto'>
            <div
              className='text-black whitespace-pre-wrap break-words font-mono'
              dangerouslySetInnerHTML={{
                __html: replaceUrlsWithLinks(displayedMessage.trim()),
              }}
            ></div>
          </div>
        )}
        {displayedFooterMessage.trim() && (
          <div className='bg-blue-100 p-4 rounded-lg shadow-md mx-4 mt-4 max-h-[1200px] overflow-y-auto'>
            <div
              className='text-black whitespace-pre-wrap break-words font-mono'
              dangerouslySetInnerHTML={{
                __html: displayedFooterMessage.trim(),
              }}
            ></div>
          </div>
        )}
      </main>
      {displayedMessage.trim() && (
        <footer className='w-full p-4 bg-gray-700 text-white flex justify-center items-center'>
          <div className='relative text-gray-600 w-96'>
            <input
              type='search'
              name='footerSearch'
              className='bg-white h-12 px-5 pr-10 pl-10 rounded-md text-sm focus:outline-none w-full shadow-md'
              value={footerSearchValue}
              onChange={handleFooterSearchChange}
              onKeyDown={(e: KeyboardEvent<HTMLInputElement>) => {
                if (e.key === 'Enter' && !footerLoading) {
                  handleFooterSearch()
                }
              }}
              placeholder='Chat about the web search with GPT-4'
              disabled={footerLoading}
            />
            <button
              type='submit'
              className='absolute right-0 top-0 mt-3 mr-4'
              onClick={handleFooterSearch}
              disabled={footerLoading}
            >
              <FontAwesomeIcon icon={faArrowRight} className='text-gray-600' />
            </button>
            <div className='absolute left-0 top-0 mt-3 ml-4'>
              <FontAwesomeIcon icon={faSearch} className='text-gray-600' />
            </div>
          </div>
          {footerLoading && (
            <div className='text-center mt-2 ml-2'>
              <FontAwesomeIcon
                icon={faSpinner}
                size='2x'
                className='text-blue-500 animate-spin'
              />
            </div>
          )}
        </footer>
      )}
    </div>
  )
}

export default App
